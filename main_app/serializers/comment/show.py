from rest_framework import serializers

from models_app.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = Comment
        fields = ["id", "text",
                  "user", "deleted_at",
                  "pub_date", "photo_id" ]