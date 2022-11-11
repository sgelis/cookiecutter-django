# Django
from django.contrib.auth.models import Group

# Third party
import pytest


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(username="superuser@foo.com", password="abc123")


@pytest.fixture
def user_alice(django_user_model):
    group_edit_own_user = Group.objects.get(name="Edit own user")
    alice = django_user_model.objects.create_user(
        username="adelorme@foo.com",
        password="abc123",
        is_staff=True,
    )
    alice.save()
    alice.groups.add(group_edit_own_user)

    return alice


@pytest.fixture
def user_bob(django_user_model):
    group_edit_own_user = Group.objects.get(name="Edit own user")
    bob = django_user_model.objects.create_user(
        username="bmaillet@foo.com",
        password="def456",
        is_staff=True,
    )
    bob.save()
    bob.groups.add(group_edit_own_user)

    return bob
