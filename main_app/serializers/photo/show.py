from rest_framework import serializers

from models_app.models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")
    img_thumbnail = serializers.CharField(source="img_thumbnail.url")
    likes_count = serializers.IntegerField()
    comments_count = serializers.IntegerField()
    is_liked = serializers.BooleanField()

    class Meta:
        model = Photo
        fields = ["id", "title",
                  "description", "img_thumbnail",
                  "user", "likes_count",
                  "comments_count", "is_liked"]