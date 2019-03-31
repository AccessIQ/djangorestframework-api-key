import pytest
from django.conf import settings


def pytest_configure():
    settings.configure(
        **dict(
            SECRET_KEY="abcd",
            INSTALLED_APPS=[
                "django.contrib.auth",
                "django.contrib.sessions",
                "django.contrib.contenttypes",
                "rest_framework",
                "rest_framework_api_key",
            ],
            ROOT_URL_CONF="urls",
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
        )
    )


@pytest.fixture
def view_with_permissions():
    from rest_framework.decorators import api_view, permission_classes
    from rest_framework.response import Response

    def create_view(*classes):
        @api_view()
        @permission_classes(classes)
        def view(*args):
            return Response()

        return view

    return create_view


def _create_api_key(**kwargs):
    from rest_framework_api_key.models import APIKey
    from rest_framework_api_key.helpers import create_secret_key

    secret_key, encoded = create_secret_key()
    api_key = APIKey.objects.create(encoded=encoded, **kwargs)
    return api_key, secret_key


def _create_user():
    from django.contrib.auth import get_user_model

    User = get_user_model()
    return User.objects.create_user(username="foo", password="bar")


@pytest.fixture
def create_request():
    from rest_framework.test import APIRequestFactory, force_authenticate

    request_factory = APIRequestFactory()

    _MISSING = object()

    def create(
        authenticated: bool = False, authorization: str = _MISSING, **kwargs
    ):
        headers = {}

        if authorization is not None:
            kwargs.setdefault("name", "test")
            api_key, secret_key = _create_api_key(**kwargs)

            if authorization is _MISSING:
                authorization = "Api-Key {api_key.name}:{secret_key}"

            authorization = authorization.format(
                api_key=api_key, secret_key=secret_key
            )

            headers["Authorization"] = authorization

        request = request_factory.get("/test/", **headers)

        if authenticated:
            user = _create_user()
            force_authenticate(request, user)

        return request

    return create
