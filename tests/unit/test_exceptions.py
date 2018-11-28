from django.http import Http404

import pytest
from bitbucket import exceptions
from requests import HTTPError, Response


class TestBitbucketExceptionToApi:
    @pytest.mark.parametrize(
        'raised_exception, expected_exception',
        [
            (exceptions.ReposNotFound, exceptions.ReposNotFoundAPIException),
            (Http404, exceptions.KatkaProjectNotFoundAPIException),
        ]
    )
    def test_katka_exceptions_mapping(self, raised_exception, expected_exception):
        with pytest.raises(expected_exception), exceptions.bitbucket_exception_to_api():
            raise raised_exception()

    @pytest.mark.parametrize(
        'response_code, expected_exception',
        [
            (401, exceptions.AuthenticationFailed),
            (403, exceptions.PermissionDenied)
        ]
    )
    def test_bitbucket_auth_errros(self, response_code, expected_exception):
        response = Response()
        response.status_code = response_code
        response._content = '{"errors":[{"message":"Some unknown problem"}]}'

        with pytest.raises(expected_exception), exceptions.bitbucket_exception_to_api():
            raise HTTPError(response=response)

    def test_bitbucket_project_not_found(self):
        response = Response()
        response.status_code = 404
        response._content = b'{"errors":[{"exceptionName":"com.atlassian.bitbucket.project.NoSuchProjectException"}]}'

        with pytest.raises(exceptions.ProjectNotFoundAPIException), exceptions.bitbucket_exception_to_api():
            raise HTTPError(response=response)

    def test_http_error_no_error_message(self):
        response = Response()
        response.status_code = 400

        with pytest.raises(exceptions.BitbucketBaseAPIException) as ex, exceptions.bitbucket_exception_to_api():
            raise HTTPError(response=response)

        assert ex.value.status_code == exceptions.BitbucketBaseAPIException.status_code
        assert str(ex.value.detail) == exceptions.BitbucketBaseAPIException.default_detail

    def test_http_no_detail(self):
        response = Response()
        response.status_code = 503
        response._content = b'{"errors":[{"message":"Some unknown problem"}]}'

        with pytest.raises(exceptions.BitbucketBaseAPIException) as ex, exceptions.bitbucket_exception_to_api():
            raise HTTPError(response=response)

        assert ex.value.status_code == exceptions.BitbucketBaseAPIException.status_code
        assert str(ex.value.detail) == exceptions.BitbucketBaseAPIException.default_detail
