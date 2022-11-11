# Django
from django.conf import settings
from django.db import migrations

# Own
from utils.migrations import create_groups

groups = {
    "Edit own user": (
        ("users", "user", "view_user"),
        ("users", "user", "change_user"),
    ),
    "Manage all users": (
        ("users", "user", "view_user"),
        ("users", "user", "add_user"),
        ("users", "user", "change_user"),
        ("users", "user", "delete_user"),
        ("users", "user", "view_all_users"),
        ("users", "user", "change_all_users"),
        ("users", "user", "view_whole_user_form"),
    ),
}


def add_groups(apps, schema_editor):
    create_groups(apps, groups)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]
