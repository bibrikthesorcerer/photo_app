from django.contrib import admin

from models_app.models import Like

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    exclude = ['deleted_at']
    list_display = ['user','photo']
    search_fields = list_display