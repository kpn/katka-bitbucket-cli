from pkgsettings import Settings

settings = Settings()
settings.configure(
    DEFAULT_BITBUCKET_SERVICE_LOCATION='https://bitbucket.org/',
    KATKA_SERVICE_LOCATION='http://katka.com/',
    CREDENTIALS_ACCESS_TOKEN_KEY='token',
)
