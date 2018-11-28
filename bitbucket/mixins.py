from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property

from guardian.mixins import PermissionRequiredMixin
from rest_framework.views import APIView

from . import serializers
from .constants import API_TO_MODEL_MAP
from .exceptions import bitbucket_exception_to_api
from .models import KatkaProject


class BitbucketPermissionRequiredMixin(PermissionRequiredMixin, APIView):
    permission_required = 'view_katkaproject'

    queryset = KatkaProject
    lookup_fields = ('katka_project_id',)
    lookup_fields_serializer = serializers.KatkaProjectSerializer

    return_403 = True
    raise_exception = True

    @cached_property
    def _object(self):
        """ Cached property to get the model object from `lookup_fields` filtered `query_string` """
        serializer = self.lookup_fields_serializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        filter = {}
        for api_field in self.lookup_fields:
            # translate api_filed name to model field name (if it's not the same)
            model_field_name = api_field if api_field not in API_TO_MODEL_MAP else API_TO_MODEL_MAP[api_field]
            filter[model_field_name] = validated_data.get(api_field)

        with bitbucket_exception_to_api():
            obj = get_object_or_404(self.queryset, **filter)
        return obj

    def get_object(self):
        return self._object

    def dispatch(self, request, *args, **kwargs):
        """ Use APIView dispatcher instead of the one from PermissionRequiredMixin """
        return APIView.dispatch(self, request, *args, **kwargs)

    def check_permissions(self, request) -> bool:
        """ Check first default permissions and then PermissionRequiredMixin(object permissions) """
        APIView.check_permissions(self, request)
        return PermissionRequiredMixin.check_permissions(self, request)
