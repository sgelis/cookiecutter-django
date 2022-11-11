# Standard library
from collections import defaultdict
from typing import DefaultDict, Dict

# Django
from django.contrib.auth.management import create_permissions
from django.contrib.contenttypes.management import create_contenttypes


def content_type_map(apps) -> DefaultDict[str, Dict[str, int]]:
    ContentType = apps.get_model("contenttypes", "ContentType")

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_contenttypes(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    ct_map: DefaultDict[str, Dict[str, int]] = defaultdict(dict)

    for content_type in ContentType.objects.all():
        ct_map[content_type.app_label][content_type.model] = content_type.id

    return ct_map


def create_groups(apps, config_perm):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    ct_map = content_type_map(apps)

    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, apps=apps, verbosity=0)
        app_config.models_module = None

    for groupname, perm_list in config_perm.items():
        group, is_new = Group.objects.get_or_create(name=groupname)
        for app_label, model, codename in perm_list:
            content_type_id = ct_map[app_label][model]
            try:
                permission = Permission.objects.get(content_type_id=content_type_id, codename=codename)
                group.permissions.add(permission)
            except Exception as e:
                print(f"\nError associating permission <{app_label}.{codename}> with group <{groupname}>: {e}")
                raise e
