from rest_framework import serializers

from models_app.models import Comment
from api.serializers.comment.show import CommentSerializer


class RetrieveCommentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id")
    user = serializers.CharField(source="user.username")
    children = CommentSerializer(many=True)
    class Meta:
        model = Comment
        fields = '__all__'