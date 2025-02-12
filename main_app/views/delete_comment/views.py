from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.utils.mixins.utils import AuthorRequiredMixin
from models_app.models import Comment
from main_app.serializers.comment import CommentSerializer

class DeleteCommentView(AuthorRequiredMixin, LoginRequiredMixin, View):
    model = Comment

    def get(self, request, **kwargs):
        comment = Comment.objects.filter(id=kwargs['id']).delete().first()
        return JsonResponse(CommentSerializer(comment).data)