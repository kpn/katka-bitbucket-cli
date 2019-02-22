import mock
import pytest
from bitbucket.conf import settings
from bitbucket.credentials import KatkaCredentialsService
from bitbucket.exceptions import BadRequestAPIException, BitbucketBaseAPIException, ProjectNotFoundAPIException
from bitbucket.service import BitbucketService
from requests import HTTPError
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied


@mock.patch('bitbucket.base.KatkaService.get')
@mock.patch('bitbucket.credentials.KatkaCredentialsService.access_token', new_callable=mock.PropertyMock)
class TestBitbucketService:
    def test_successful(self, mock_access_token, mock_get_request):
        result = mock.Mock()
        result.json.return_value = {'key', 'value'}
        mock_get_request.return_value = result
        mock_access_token.return_value = 'some_access_token'

        with settings(DEFAULT_BITBUCKET_SERVICE_LOCATION='https://bb-8.org/'):
            bitbucket_service = BitbucketService(credentials_provider=KatkaCredentialsService(request=mock.Mock()))

        service_result = bitbucket_service.get(params={'key': 'value'})

        assert bitbucket_service.base_path
        assert bitbucket_service.base_url == 'https://bb-8.org'  # test use default bitbucket location and rstrip
        assert bitbucket_service.client.headers['Authorization'] == 'Bearer some_access_token'

        assert service_result == {'key', 'value'}

        mock_get_request.assert_called_once_with('https://bb-8.org/rest/api/1.0/', params={'key': 'value'})
        result.raise_for_status.assert_called_once()

    @pytest.mark.parametrize(
        'bitbucket_exception, api_exception',
        (
            (HTTPError(response=mock.Mock(status_code=500, content=None)), BitbucketBaseAPIException),
            (HTTPError(response=mock.Mock(status_code=401, content=None)), AuthenticationFailed),
            (HTTPError(response=mock.Mock(status_code=403, content=None)), PermissionDenied),
            (HTTPError(response=mock.Mock(status_code=400, content=None)), BadRequestAPIException),
            (HTTPError(response=mock.Mock(status_code=404, content=None)), NotFound),
            (
                HTTPError(
                    response=mock.Mock(
                        status_code=404,
                        json=lambda: {
                            'errors': [{'exceptionName': 'com.atlassian.bitbucket.project.NoSuchProjectException'}]
                        }
                    )
                ),
                ProjectNotFoundAPIException
            ),
            (
                HTTPError(
                    response=mock.Mock(
                        status_code=500,
                        json=lambda: {
                            'errors': [{'exceptionName': 'Some unexpected exception name'}]
                        }
                    )
                ),
                BitbucketBaseAPIException
            ),
        )
    )
    def test_bitbucket_service_exception(self, mock_access_token, mock_get_request,
                                         bitbucket_exception, api_exception):
        result = mock.Mock()
        result.raise_for_status.side_effect = bitbucket_exception
        mock_get_request.return_value = result

        bitbucket_service = BitbucketService(
            limit=2, start=0,
            base_url='https://test.com'
        )

        with pytest.raises(api_exception):
            bitbucket_service.get()

        assert bitbucket_service.base_url == 'https://test.com'  # test use given bitbucket location and rstrip
