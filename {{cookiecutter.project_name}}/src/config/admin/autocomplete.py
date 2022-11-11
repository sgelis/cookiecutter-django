# Standard library
from typing import Tuple

# Django
from django.apps import apps
from django.contrib.admin import ModelAdmin
from django.contrib.admin.views.autocomplete import AutocompleteJsonView
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.http import Http404, HttpRequest, JsonResponse


class SimplerAutocompleteJsonView(AutocompleteJsonView):
    """Simpler Autocomplete view for Django admin.

    Simpler version of an autocomplete endpoint that offers suggestions for a given model, and does not need to be
    linked to a remote model/form/field/whatever.
    """

    def get(self, request, *args, **kwargs) -> JsonResponse:
        """Heavily inspired by parent's method. Simplified for our needs.

        Returns:
            A JsonResponse with search results of the form:

                {
                    results: [{id: "123" text: "foo"}],
                    pagination: {more: true}
                }

        Raises:
            PermissionDenied: User does not have permission to list objects of this model.
        """
        self.term, self.model_admin, value_field = self.process_request(request)

        if not self.has_perm(request):
            raise PermissionDenied

        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return JsonResponse(
            {
                "results": [
                    {"pk": str(obj.pk), "id": str(getattr(obj, value_field)), "text": str(obj)}
                    for obj in context["object_list"]
                ],
                "pagination": {"more": context["page_obj"].has_next()},
            }
        )

    def get_queryset(self) -> QuerySet:
        """Heavily inspired by parent's method. Simplified for our needs.

        Returns:
            A QuerySet of relevant objects for the requested model.
        """
        qs = self.model_admin.get_queryset(self.request)
        qs, search_use_distinct = self.model_admin.get_search_results(self.request, qs, self.term)
        if search_use_distinct:  # pragma: no cover  # hard to test and Django is already supposed to test it
            qs = qs.distinct()
        return qs

    def process_request(self, request: HttpRequest) -> Tuple[str, ModelAdmin, str]:
        """Heavily inspired by parent's method. Simplified for our needs.

        Returns:
            A tuple containing (term, model_admin, value_field), where:

                - term: the search term entered by user.
                - model_admin: the ModelAdmin object corresponding to the requested model name.
                - value_field: the value field that will be used to put object IDs in the JSON response (additionnaly to
                  their PK).

        Raises:
            PermissionDenied: Missing GET param or model does not exist or ModelAdmin does not exist for this model.
            Http404: ModelAdmin has not declared `search_fields`.
        """
        term = request.GET.get("term", "")

        try:
            app_label = request.GET["app_label"]
            model_name = request.GET["model_name"]
            value_field = request.GET["value_field"]
        except KeyError as e:
            raise PermissionDenied from e

        # Retrieve objects from parameters.
        try:
            remote_model = apps.get_model(app_label, model_name)
        except LookupError as e:
            raise PermissionDenied from e

        try:
            model_admin = self.admin_site._registry[remote_model]  # type: ignore  # self.admin_site exists
        except KeyError as e:  # pragma: no cover  # hard to test and Django is already supposed to test it
            raise PermissionDenied from e

        # Validate suitability of objects.
        if not model_admin.get_search_fields(
            request
        ):  # pragma: no cover  # hard to test and Django is already supposed to test it
            raise Http404(f"{type(model_admin).__qualname__} must have search_fields for the autocomplete_view.")

        return term, model_admin, value_field
