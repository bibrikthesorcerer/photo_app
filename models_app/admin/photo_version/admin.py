from django.contrib import admin
from imagekit.admin import AdminThumbnail

from ...models import PhotoVersion


@admin.register(PhotoVersion)
class PhotoVersionAdmin(admin.ModelAdmin):
    list_display = ["title", "photo__id", "photo", "admin_thumbnail", "photo__user__username"]
    search_fields = ["title", "author", "description"]
    admin_thumbnail = AdminThumbnail(image_field="admin_thumbnail")
    list_filter = ["photo__user__username", "photo__title", "created_at", "photo__status"]