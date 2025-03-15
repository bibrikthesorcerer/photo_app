from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from models_app.models import Like
from models_app.utils import DeletedAtFilter


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]
    list_display = ["user", "photo", "formatted_deleted_at"]
    search_fields = ["user", "photo"]
    list_filter = [DeletedAtFilter, "user", "photo", "updated_at", "deleted_at", "created_at"]

    def formatted_deleted_at(self, obj):
        return obj.deleted_at if obj.deleted_at else "No"
    formatted_deleted_at.short_description="Deleted Status"
