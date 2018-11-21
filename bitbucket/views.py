from bitbucket.exceptions import bitbucket_exception_to_api
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .repos import BitbucketRepos


class BitbucketReposView(APIView):
    serializer_class = serializers.BitbucketRepos

    # TODO: add permissions and auth classes

    def get(self, request, project_id):
        data = request.data
        if request.query_params.get('limit') is not None:
            data['limit'] = request.query_params.get('limit')
        if request.query_params.get('start') is not None:
            data['start'] = request.query_params.get('start')
        data.update(
            {
                'katka_project_id': request.query_params.get('katka_project_id'),
                'project_id': project_id,
            }
        )

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        with bitbucket_exception_to_api():
            resp = BitbucketRepos(**validated_data).get_repos()

        return Response(data=resp)


class BitbucketRepoView(APIView):
    def get(self, request, project_id, repo_name=None):
        # TODO implement view to retrieve specific repo information
        return Response()
