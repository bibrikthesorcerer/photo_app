from rest_framework import serializers

from models_app.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    img_thumbnail = serializers.CharField(source="img_thumbnail.url")
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField(required=False)

    class Meta:
        model = Photo
        fields = ["id", "title","description", "img_thumbnail", "img",
                  "status", "created_at","updated_at", "pub_date",
                  "user", "likes_count", "comments_count", "is_liked"]
