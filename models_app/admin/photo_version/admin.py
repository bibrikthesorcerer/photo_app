from django.contrib import admin
from imagekit.admin import AdminThumbnail

from ...models import PhotoVersion

@admin.register(PhotoVersion)
class PhotoVersionAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo_id', 'author']
    search_fields = ['title', 'author', 'description']
    admin_thumbnail = AdminThumbnail(image_field='admin_thumbnail')

    @admin.display(description="Author")
    def author(self, obj):
        return f'{obj.photo.user.username}'

    @admin.display(description="Photo ID")
    def photo_id(self, obj):
        return f'{obj.photo.id}'