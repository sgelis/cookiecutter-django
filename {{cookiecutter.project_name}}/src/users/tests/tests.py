# Django
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, make_password
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.utils.translation import gettext

# Third party
import pytest

# Own
from config.admin.sites import CustomAdminSite
from utils.typing import AuthenticatedWSGIRequest
from ..admin import CustomUserAdmin
from ..fields import TokenWidget
from ..forms import CustomUserChangeForm
from ..models import CustomUserManager

User = get_user_model()


class TestUserModel:
    def test_normalize_username_str(self):
        username = "ToToLeRiGoLo@FoO.cOm"
        assert User.normalize_username(username) == username.lower()

    def test_normalize_username_bytes(self):
        username = b"ToToLeRiGoLo@FoO.cOm"
        assert User.normalize_username(username) == username


@pytest.mark.django_db
class TestUserManager:
    def test_normalize_email_non_empty(self):
        email = "ToToLeRiGoLo@FoO.cOm"
        assert CustomUserManager.normalize_email(email) == email.lower()

    def test_normalize_email_empty(self):
        email = None
        assert CustomUserManager.normalize_email(email) == ""

    def test_can_create_user_without_email(self):
        """
        Does not test the method thoroughly as it is derived from Django's, only tests that things are not utterly
        broken and that users can still be created without email field.
        """
        user = User.objects.create_user(username="charles@foo.com", password="ghi789")
        assert User.objects.get(username="charles@foo.com") == user

    def test_can_create_superuser_without_email(self):
        """
        Does not test the method thoroughly as it is derived from Django's, only tests that things are not utterly
        broken and that superusers can still be created without email field.
        """
        user = User.objects.create_superuser(username="charles@foo.com", password="ghi789")
        assert User.objects.get(username="charles@foo.com") == user
        assert user.is_superuser


class TestUserAdmin:
    def setup_method(self):
        self.admin = CustomUserAdmin(User, CustomAdminSite())

    @pytest.mark.django_db
    def test_response_change_applies_language(self, client, user_alice):
        client.force_login(user_alice, "django.contrib.auth.backends.ModelBackend")
        response = client.post(
            reverse("admin:users_user_change", args=(user_alice.pk,)),
            {
                "username": user_alice.username,
                "access_token": "",
                "first_name": user_alice.first_name,
                "last_name": user_alice.last_name,
                "language": "fr-ch",
                "_save": "Save",
            },
        )
        assert response.cookies["django_language"].value == "fr-ch"

    @pytest.mark.django_db
    def test_get_fieldsets_unprivileged(self, rf, user_alice):
        all_fieldsets = self.admin.fieldsets
        request = rf.get(reverse("admin:users_user_change", args=(user_alice.pk,)))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        fieldsets = self.admin.get_fieldsets(request, user_alice)
        assert len(fieldsets) == len(all_fieldsets) - 2

    @pytest.mark.django_db
    def test_get_fieldsets_privileged(self, rf, user_alice):
        all_fieldsets = self.admin.fieldsets
        perm = Permission.objects.get(
            content_type__app_label="users", content_type__model="user", codename="view_whole_user_form"
        )
        user_alice.user_permissions.add(perm)
        request = rf.get(reverse("admin:users_user_change", args=(user_alice.pk,)))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        fieldsets = self.admin.get_fieldsets(request, user_alice)
        assert len(fieldsets) == len(all_fieldsets)

    @pytest.mark.django_db
    def test_get_queryset_unprivileged(self, rf, user_superuser, user_alice, user_bob):
        request = rf.get(reverse("admin:users_user_changelist"))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        qs = self.admin.get_queryset(request)
        # Unprivileged users can only see themselves
        assert len(qs) == 1
        assert qs[0] == user_alice

    @pytest.mark.django_db
    def test_get_queryset_privileged(self, rf, user_superuser, user_alice, user_bob):
        perm = Permission.objects.get(
            content_type__app_label="users", content_type__model="user", codename="view_all_users"
        )
        user_alice.user_permissions.add(perm)
        request = rf.get(reverse("admin:users_user_changelist"))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        qs = self.admin.get_queryset(request).order_by("username")
        # Privileged users can see all users except superusers
        assert len(qs) == 2
        assert qs[0] == user_alice
        assert qs[1] == user_bob

    @pytest.mark.django_db
    def test_get_queryset_superuser(self, rf, user_superuser, user_alice, user_bob):
        request = rf.get(reverse("admin:users_user_changelist"))
        request.user = user_superuser
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        qs = self.admin.get_queryset(request).order_by("username")
        # Superusers can see all users
        assert len(qs) == 3
        assert qs[0] == user_alice
        assert qs[1] == user_bob
        assert qs[2] == user_superuser

    @pytest.mark.django_db
    def test_get_readonly_fields_non_superuser(self, rf, user_alice):
        perm = Permission.objects.get(
            content_type__app_label="users", content_type__model="user", codename="view_whole_user_form"
        )
        user_alice.user_permissions.add(perm)
        request = rf.get(reverse("admin:users_user_change", args=(user_alice.pk,)))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        ro_fields = self.admin.get_readonly_fields(request, user_alice)
        assert "is_superuser" in ro_fields

    @pytest.mark.django_db
    def test_get_readonly_fields_superuser(self, rf, user_superuser, user_alice):
        request = rf.get(reverse("admin:users_user_change", args=(user_alice.pk,)))
        request.user = user_superuser
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        ro_fields = self.admin.get_readonly_fields(request, user_alice)
        assert "is_superuser" not in ro_fields

    @pytest.mark.django_db
    def test_has_change_permission_unprivileged_self_edit(self, rf, user_alice):
        """
        Alice is allowed to edit herself
        """
        request = rf.get(reverse("admin:users_user_change", args=(user_alice.pk,)))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        perm = self.admin.has_change_permission(request, user_alice)
        assert perm is True

    @pytest.mark.django_db
    def test_has_change_permission_unprivileged_self_edit(self, rf, user_alice, user_bob):
        """
        Alice is not allowed to edit other users
        """
        request = rf.get(reverse("admin:users_user_change", args=(user_bob.pk,)))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        perm = self.admin.has_change_permission(request, user_bob)
        assert perm is False

    @pytest.mark.django_db
    def test_has_change_permission_unprivileged_self_edit(self, rf, user_alice, user_bob):
        """
        Privileged non-super users can edit other users
        """
        perm = Permission.objects.get(
            content_type__app_label="users", content_type__model="user", codename="change_all_users"
        )
        user_alice.user_permissions.add(perm)
        request = rf.get(reverse("admin:users_user_change", args=(user_bob.pk,)))
        request.user = user_alice
        request = AuthenticatedWSGIRequest.from_WSGIRequest(request)
        perm = self.admin.has_change_permission(request, user_bob)
        assert perm is True


class TestUserChangeForm:
    @pytest.mark.django_db
    def test_empty_val_leaves_token_untouched(self, user_alice):
        # No initial token, no new token (`None`)
        form = CustomUserChangeForm(instance=user_alice)
        assert form.clean_access_token() == form.initial["access_token"] == ""

        # No initial token, no new token (empty string)
        form = CustomUserChangeForm(instance=user_alice, data={"access_token": ""})
        assert form.clean_access_token() == form.initial["access_token"] == ""

        access_token = make_password("def_456")
        user_alice.access_token = access_token
        user_alice.save()
        # Initial token set, no new token (`None`)
        form = CustomUserChangeForm(instance=user_alice)
        assert form.clean_access_token() == form.initial["access_token"] == access_token

        # Initial token set, no new token (empty string)
        form = CustomUserChangeForm(instance=user_alice, data={"access_token": ""})
        assert form.clean_access_token() == form.initial["access_token"] == access_token

    def test_non_empty_val(self, user_alice, settings):
        # No initial token
        raw_access_token = "def456"
        access_token = make_password(raw_access_token, settings.SECRET_KEY)
        form = CustomUserChangeForm(instance=user_alice, data={"access_token": raw_access_token})
        form.full_clean()
        clean_access_token = form.clean_access_token()
        assert clean_access_token != form.initial["access_token"]
        assert clean_access_token == access_token

        user_alice.access_token = access_token
        user_alice.save()

        # Initial token set, new token provided
        new_raw_access_token = "ghi678"
        new_access_token = make_password(new_raw_access_token, settings.SECRET_KEY)
        form = CustomUserChangeForm(instance=user_alice, data={"access_token": new_raw_access_token})
        form.full_clean()
        clean_access_token = form.clean_access_token()
        assert clean_access_token != form.initial["access_token"]
        assert clean_access_token == new_access_token


class TestTokenWidget:
    def setup_method(self):
        self.widget = TokenWidget()

    def test_get_context_no_token_set(self):
        context = self.widget.get_context("name", "", {"class": "baz"})
        assert context["summary"] == [{"label": gettext("No token set.")}]

    def test_get_context_token_set(self):
        val = make_password("def456")
        context = self.widget.get_context("name", val, {"class": "baz"})
        labels = sorted([d["label"] for d in context["summary"]])
        expected_labels_en = ["algorithm", "block size", "hash", "parallelism", "salt", "work factor"]
        expected_labels = sorted([gettext(label) for label in expected_labels_en])
        assert labels == expected_labels

    def test_get_context_invalid_hash_algorithm(self):
        val = make_password("def456")
        # Remove a handful of leading characters of the hashed token to make it invalid
        messed_up_val = val[10:]
        context = self.widget.get_context("name", messed_up_val, {"class": "baz"})
        assert context["summary"] == [{"label": gettext("Invalid token format or unknown hashing algorithm.")}]

    def test_get_context_invalid_password_prefix(self):
        val = f"{UNUSABLE_PASSWORD_PREFIX}foo"
        context = self.widget.get_context("name", val, {"class": "baz"})
        assert context["summary"] == [{"label": gettext("No token set.")}]
