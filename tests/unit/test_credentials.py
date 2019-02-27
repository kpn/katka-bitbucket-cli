import mock
import pytest
from bitbucket.conf import settings
from bitbucket.credentials import KatkaCredentialsService
from bitbucket.exceptions import BitbucketBaseAPIException
from requests import HTTPError
from rest_framework.exceptions import PermissionDenied


@mock.patch('bitbucket.base.KatkaService.get')
class TestKatkaCredentialsService:
    def test_get_access_token(self, mock_katka_service_get):
        response = mock.Mock()
        response.json.return_value = {
            'credential': '196bce31-2b88-4941-a858-857977d07e8b',
            'secret_public_identifier': '3aa0815d-4dcb-4ba9-929e-c377cf038bd2',
            'value': 'the big secret!!!'
        }
        mock_katka_service_get.return_value = response

        with settings(KATKA_SERVICE_LOCATION='https://r2-d2.com/'):
            katka_credentials_service = KatkaCredentialsService(
                request=mock.Mock(auth='bt'), credential='wonder_women'
            )

        assert katka_credentials_service.base_url == 'https://r2-d2.com'
        assert katka_credentials_service.base_path == 'credentials'
        assert katka_credentials_service.bearer_token == 'bt'

        assert katka_credentials_service.access_token == 'the big secret!!!'

    @pytest.mark.parametrize(
        'katka_exception, api_exception',
        (
            (HTTPError(response=mock.Mock(status_code=500, content=None)), BitbucketBaseAPIException),
            (HTTPError(response=mock.Mock(status_code=401, content=None)), PermissionDenied),
        )
    )
    def test_katka_service_exception(self, mock_katka_service_get, katka_exception, api_exception):
        response = mock.Mock()
        response.raise_for_status.side_effect = katka_exception
        mock_katka_service_get.return_value = response

        katka_credentials_service = KatkaCredentialsService(
            request=mock.Mock(auth='bt'), credential='wonder_women'
        )

        with pytest.raises(api_exception):
            katka_credentials_service.access_token
