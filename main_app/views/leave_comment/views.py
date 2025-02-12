from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.services.comment import CreateComment
from main_app.serializers.comment import CommentSerializer

class LeaveCommentView(LoginRequiredMixin, View):

    def post(self, request):
        result, instance = CreateComment().execute({
            'photo_id': request.POST.get('photo'),
            'parent_id': request.POST.get('parent'),
            'user': request.user,
            'text': request.POST.get('text'),
        })
        return JsonResponse(CommentSerializer(instance).data)