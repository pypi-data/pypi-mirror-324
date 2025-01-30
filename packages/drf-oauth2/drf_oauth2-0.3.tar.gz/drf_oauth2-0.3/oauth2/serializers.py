from rest_framework import serializers


class SocialAuthSerializer(serializers.Serializer):
    provider = serializers.CharField(required=True)
    code = serializers.CharField(required=False)
