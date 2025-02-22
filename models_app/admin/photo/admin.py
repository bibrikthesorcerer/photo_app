from django.contrib import admin
from imagekit.admin import AdminThumbnail

from models_app.models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'admin_thumbnail']
    search_fields = list_display + ['description']
    admin_thumbnail = AdminThumbnail(image_field='admin_thumbnail')