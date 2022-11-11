# Django REST Framework
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

# Third party
from drf_spectacular.utils import OpenApiExample, extend_schema


class Ping(mixins.RetrieveModelMixin, mixins.CreateModelMixin, APIView):
    permission_classes = ()

    # noinspection PyMethodMayBeStatic
    @extend_schema(
        request={},
        responses={200: "pong"},
        examples=[
            OpenApiExample("Ping", response_only=True, summary="Ping", value="pong", status_codes=["200"]),
        ],
    )
    def get(self, request: Request, format=None) -> Response:
        """Software ping with `GET`."""
        return Response("pong")

    # noinspection PyMethodMayBeStatic
    @extend_schema(
        request={},
        responses={200: "pong"},
        examples=[
            OpenApiExample("Ping", response_only=True, summary="Ping", value="pong", status_codes=["200"]),
        ],
    )
    def post(self, request: Request, format=None) -> Response:
        """Software ping with `POST`"""
        return Response("pong")
