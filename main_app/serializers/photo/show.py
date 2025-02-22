from rest_framework import serializers
from django.core.paginator import Page

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
        
class PhotoPageSerializer(serializers.Serializer):
    photos_page = PhotoSerializer(many=True, source='object_list')
    total_pages = serializers.IntegerField(source='paginator.num_pages')
    current_page = serializers.IntegerField(source='number')
    has_next = serializers.BooleanField()
    has_previous = serializers.BooleanField()
