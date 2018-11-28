import mock
import pytest
from bitbucket.service import BitbucketService
from requests import HTTPError


class TestBitbucketService:
    def test_no_access_token(self):
        service = BitbucketService(katka_project=mock.Mock(oauth_access_token=None))

        assert service.oauth_access_token is None

    @mock.patch('requests.sessions.Session.get')
    def test_successful(self, mock_get_request, settings):
        result = mock.Mock()
        result.json.return_value = {'key', 'value'}
        mock_get_request.return_value = result
        settings.SERVICE_BITBUCKET_LOCATION = 'https://bitbucket-url.com'
        settings.REQUESTS_CA_BUNDLE = 'path_for_ca_bundle'

        bitbucket_service = BitbucketService(katka_project=mock.Mock(oauth_access_token='some_access_token'))
        service_result = bitbucket_service.get(params={'key': 'value'})

        assert bitbucket_service.base_url
        assert bitbucket_service.base_path
        assert not bitbucket_service.path
        assert bitbucket_service.client.headers['Authorization'] == 'Bearer some_access_token'

        assert service_result == {'key', 'value'}
        mock_get_request.assert_called_once_with(
            'https://bitbucket-url.com/rest/api/1.0/', params={'key': 'value'}, verify='path_for_ca_bundle'
        )
        result.raise_for_status.assert_called_once()

    @mock.patch('requests.sessions.Session.get')
    def test_http_error(self, mock_get_request, settings):
        mock_get_request.side_effect = HTTPError
        settings.SERVICE_BITBUCKET_LOCATION = 'https://bitbucket-url.com'
        settings.REQUESTS_CA_BUNDLE = 'path_for_ca_bundle'

        bitbucket_service = BitbucketService(
            katka_project=mock.Mock(oauth_access_token='some_access_token'), limit=2, start=0
        )

        with pytest.raises(HTTPError):
            bitbucket_service.get()

        mock_get_request.assert_called_once_with(
            'https://bitbucket-url.com/rest/api/1.0/', params={'limit': 2, 'start': 0}, verify='path_for_ca_bundle'
        )
