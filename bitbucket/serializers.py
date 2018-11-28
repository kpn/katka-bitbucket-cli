from rest_framework import serializers


class KatkaProjectSerializer(serializers.Serializer):
    katka_project_id = serializers.UUIDField(required=True)


class BitbucketSerializer(serializers.Serializer):
    limit = serializers.IntegerField(min_value=0, required=False)
    start = serializers.IntegerField(min_value=0, required=False)


class BitbucketReposSerializer(BitbucketSerializer):
    project_id = serializers.CharField(required=True)
