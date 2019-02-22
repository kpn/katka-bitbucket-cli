import mock
import pytest
from bitbucket.base import KatkaService
from bitbucket.exceptions import BitbucketBaseAPIException
from requests import RequestException


class TestKatkaService:
    @mock.patch('bitbucket.base.requests')
    def test_get_successful(self, mock_requests):
        response = mock.Mock()
        session = mock.Mock(headers={})
        session.get.return_value = response
        mock_requests.Session.return_value = session

        katka_service = KatkaService(bearer_token='bt')

        assert katka_service.client.headers == {
            'Accept': 'application/json',
            'User-Agent': 'katka',
            'Authorization': 'Bearer bt'
        }
        assert katka_service.get('https://storm.com/') == response

    @pytest.mark.parametrize(
        'call_exception, api_exception',
        (
            (IOError(), BitbucketBaseAPIException),
            (RequestException(), BitbucketBaseAPIException),
        )
    )
    @mock.patch('bitbucket.base.KatkaService.client', new_callable=mock.PropertyMock)
    def test_get_exception(self, mock_katka_service_client, call_exception, api_exception):
        client = mock.Mock()
        client.get.side_effect = call_exception
        mock_katka_service_client.return_value = client

        with pytest.raises(api_exception):
            KatkaService().get('https://storm.com/')
