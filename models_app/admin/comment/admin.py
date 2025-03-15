from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from models_app.models import Comment
from models_app.admin.comment.forms import CommentForm
from models_app.utils import DeletedAtFilter


class IsRoot(admin.SimpleListFilter):
    title = _('Is Root')
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        return (
            ('root', _('Root')),
            ('not_root', _('Not Root')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'root':
            return queryset.filter(parent__isnull=True)
        if self.value() == 'not_root':
            return queryset.filter(parent__isnull=False)
        return queryset


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]
    list_display = ["text", "user", "photo", "formatted_is_root", "parent_id", "parent"]
    search_fields = ["text"]
    list_filter = [IsRoot, DeletedAtFilter,"user", "photo", "updated_at", "created_at", "deleted_at"]
    form = CommentForm

    def formatted_is_root(self, obj):
        return "No" if obj.parent else "Yes"
    formatted_is_root.short_description="Is Root"
