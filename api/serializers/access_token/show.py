from rest_framework import serializers


class ShowAccessTokenSerializer(serializers.Serializer):
    created = serializers.DateTimeField()
    token = serializers.CharField()