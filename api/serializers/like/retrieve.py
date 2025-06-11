from rest_framework import serializers

from models_app.models import Like


class RetrieveLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"