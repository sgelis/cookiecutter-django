# Third party
import pytest

# Own
from config.admin import CustomAdminSite
from core.admin import SettingsAdmin
from core.models import Settings


@pytest.fixture
def settings_admin():
    return SettingsAdmin(Settings, CustomAdminSite())
