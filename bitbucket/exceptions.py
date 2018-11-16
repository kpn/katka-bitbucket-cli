import logging
from contextlib import contextmanager

from bitbucket.models import KatkaProject
from requests import HTTPError
from rest_framework.exceptions import APIException, AuthenticationFailed, NotFound, PermissionDenied


class ReposNotFound(Exception):
    pass


class BitbucketBaseAPIException(APIException):
    def __init__(self, detail=None, code=None, status_code=None):
        super().__init__(detail, code)
        if status_code:
            self.status_code = status_code


class ReposNotFoundAPIException(NotFound):
    default_detail = 'No repos found for that project_id'


class ProjectNotFoundAPIException(NotFound):
    default_detail = 'Project not found'


@contextmanager
def bitbucket_exception_to_api():
    try:
        yield
    except ReposNotFound:
        raise ReposNotFoundAPIException()
    except KatkaProject.DoesNotExist:
        raise ProjectNotFoundAPIException()
    except HTTPError as ex:
        if ex.response.status_code == 401:
            raise AuthenticationFailed()

        if ex.response.status_code == 403:
            raise PermissionDenied()

        errors = ex.response.json().get('errors') if ex.response.content else None

        if errors and errors[0].get('exceptionName') == 'com.atlassian.bitbucket.project.NoSuchProjectException':
            logging.warning(errors[0].get('message'))
            raise ProjectNotFoundAPIException()

        if errors:
            logging.exception(f'Unexpected Bitbucket exception: {errors[0].get("message")}')
        else:
            logging.exception(f'Unexpected Bitbucket exception: {str(ex)}')

        raise BitbucketBaseAPIException(status_code=ex.response.status_code)
