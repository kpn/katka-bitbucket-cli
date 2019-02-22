from bitbucket.conf import settings


def pytest_configure():
    d = dict(
        DEFAULT_BITBUCKET_SERVICE_LOCATION='https://bitbucket.org/',
        KATKA_SERVICE_LOCATION='http://katka.com/',
        CREDENTIALS_ACCESS_TOKEN_KEY='token',
    )

    settings.configure(**d)
