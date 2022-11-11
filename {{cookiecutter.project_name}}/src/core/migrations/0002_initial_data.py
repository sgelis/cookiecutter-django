# Django
from django.conf import settings
from django.db import migrations


def add_settings(apps, schema_editor):
    Settings = apps.get_model("core", "settings")
    Settings().save()


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.RunPython(add_settings),
    ]
