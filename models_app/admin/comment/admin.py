from django.contrib import admin

from ...models import Comment
from models_app.admin.comment.forms import CommentForm


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    exclude = ["deleted_at"]
    list_display = ["text", "user", "photo", "parent"]
    search_fields = list_display
    form = CommentForm
