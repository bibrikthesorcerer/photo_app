from rest_framework import serializers

from models_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    user = serializers.CharField(source="user.username")
    class Meta:
        model = Comment
        exclude = ['deleted_at']
