"""Test the HasAPIKey permission class."""

import pytest

from rest_framework_api_key.permissions import HasAPIKey

pytestmark = pytest.mark.django_db


@pytest.fixture(name="view")
def fixture_view(view_with_permissions):
    return view_with_permissions(HasAPIKey)


def test_if_valid_api_key_then_permission_granted(create_request, view):
    request = create_request()
    response = view(request)
    assert response.status_code == 200


def test_if_no_api_key_then_permission_denied(create_request, view):
    request = create_request(authorization=None)
    response = view(request)
    assert response.status_code == 403


@pytest.mark.parametrize(
    "authorization",
    [
        "foo",
        "Content-Type: text/plain",
        "Api-Key:",
        "Api-Key foo",
        "Api-Key :bar",
    ],
)
def test_if_junk_api_key_then_permission_denied(
    create_request, view, authorization
):
    request = create_request(authorization=authorization)
    response = view(request)
    assert response.status_code == 403


def test_if_revoked_then_permission_denied(create_request, view):
    request = create_request(revoked=True)
    response = view(request)
    assert response.status_code == 403


def test_if_invalid_secret_key_then_permission_denied(create_request, view):
    request = create_request(authorization="Api-Key {api_key.name}:abcd")
    response = view(request)
    assert response.status_code == 403


def test_if_invalid_name_then_permission_denied(create_request, view):
    request = create_request(authorization="Api-Key foo:{secret_key}")
    response = view(request)
    assert response.status_code == 403
