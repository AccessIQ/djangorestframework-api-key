# djangorestframework-api-key


[![license](https://img.shields.io/pypi/l/djangorestframework-api-key.svg)][pypi-url]
[![pypi](https://img.shields.io/pypi/v/djangorestframework-api-key.svg)][pypi-url]
[![travis](https://img.shields.io/travis-ci/florimondmanca/djangorestframework-api-key.svg)][travis-url]

[![python](https://img.shields.io/pypi/pyversions/djangorestframework-api-key.svg)][pypi-url]
[![django](https://img.shields.io/pypi/djversions/djangorestframework-api-key.svg?colorB=44b78b)][pypi-url]
[![drf](https://img.shields.io/badge/drf-3.8+-7f2d2d.svg)][pypi-url]

🔐 Web API permissions for the [Django REST Framework](http://www.django-rest-framework.org).

This project is based on (yet not a fork of) the unmaintained [django-rest-framework-api-key](https://github.com/manosim/django-rest-framework-api-key) project.

## Features

**Allow service clients to safely use your API**.

A service client may be a frontend app, a third-party API or any non-human service which does not have a user account but needs to interact with your API.

Intended to be:

- ✌️ **Simple to use**: create, manage and revoke API keys via the admin site.
- 🔒 **Safe**: the key is only visible at creation and never shown again.

## Caveats

[API Keys ≠ Security](https://nordicapis.com/why-api-keys-are-not-enough/): depending on your situation, you should probably not rely on API keys only to authenticate/authorize your clients. Doing so shifts the responsability of information security on your clients. This induces risks, especially if detaining an API key gives access to confidential information or write operations.

As a general advice, **allow only those who require resources to access those specific resources**. If your non-user client only needs to access a specific endpoint, add API permissions on that endpoint only.

Act responsibly.

## Install

- Install from PyPI:

```bash
$ pip install djangorestframework-api-key
```

- Add the app to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
  # ...,
  'rest_framework',
  'rest_framework_api_key',
]
```

Run the included migrations:

```bash
$ python manage.py migrate
```

## Usage

### Setting permissions

This package provides permission classes to allow external clients to use your API.

- `HasAPIKey`: this permission class requires **all clients** to provide a valid API key, regardless of whether they provide authentication details.
- `HasAPIKeyOrIsAuthenticated`: if you want to allow clients to provide either an API key or authentication credentials, use this permission class instead.

As with every permission class, you can either use them globally:

```python
# settings.py

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework_api_key.permissions.HasAPIKey',
    ]
}
```

or on a per-view basis:

```python
# views.py
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView

class UserListView(APIView):
    permission_classes = (HasAPIKey,)
    # ...
```

Refer to [DRF Docs - Setting the permission policy](http://www.django-rest-framework.org/api-guide/permissions/#setting-the-permission-policy) for more information on using permission classes.

### Making authorized requests

Once API key permissions are enabled on your API, clients can pass their API key via the `Api-Key` header (this is customizable, see [Settings](#settings)):

```bash
$ curl -H 'Api-Key: YOUR_API_KEY_HERE' http://localhost:8000/my-resource/
```

## Settings

`API_KEY_HEADER`:

- Name of the header which clients use to pass their API key.
- Default value: `HTTP_API_KEY` (which means clients should use the `Api-Key` header — see the [docs on HttpRequest.META](https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META)).

## Example project

See the [example project](https://github.com/florimondmanca/djangorestframework-api-key-example) for showcase usage in the context of a Django project.

## Development

This section is aimed at developers and maintainers.

### Install

Installing locally requires [Pipenv](https://github.com/pypa/pipenv) and Python 3.7.

1. Fork the repo
2. Clone it on your local
3. Install dependencies with Pipenv: `$ pipenv install --dev`
4. Activate using `$ pipenv shell`

### Tests

Run the tests using:

```bash
$ python runtests.py
```

### Generating migrations

This package includes migrations. To update them in case of changes without setting up a Django project, run:

```bash
$ python makemigrations.py rest_framework_api_key
```

### CI/CD - Releases

Travis CI is in use to automatically:

- Test the package on supported versions of Python and Django.
- Release *tagged commits* to PyPI.

See `.travis.yml` for further details.

<!-- URLs -->

[travis-url]: https://travis-ci.org/florimondmanca/djangorestframework-api-key

[pypi-url]: https://pypi.org/project/djangorestframework-api-key/
