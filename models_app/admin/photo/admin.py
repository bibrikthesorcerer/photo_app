from django.contrib import admin
from ...models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status']
    search_fields = list_display + ['description']