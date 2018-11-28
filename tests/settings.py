# -*- coding: utf-8
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't)c0g-tbhgoe2ybv4(iyj%!07*si)co@rg21f&ejm3v=)u^_-8'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'bitbucket.urls'

FIELD_ENCRYPTION_KEY = 'SURdYnt6gHdgq84TgewXS6WayBQYlHt9Lr8Sryv9yOI='

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'bitbucket',

    'encrypted_model_fields',
    'guardian',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Django Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


REQUESTS_CA_BUNDLE = "/etc/ssl/certs/ca-certificates.crt"

# Bitbucket service
SERVICE_BITBUCKET_LOCATION = 'https://bitbucket.org/'
