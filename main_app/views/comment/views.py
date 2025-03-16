from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.serializers.comment import CommentSerializer
from main_app.services import CreateComment, ListThread, DeleteComment, SendCommentNotification


class DeleteCommentView(LoginRequiredMixin, View):

    def post(self, request, **kwargs):
        comment, is_deleted = DeleteComment.execute({**request.POST.dict()})
        data = CommentSerializer(comment).data
        data.update({'is_deleted':is_deleted})
        return JsonResponse(data)


class LeaveCommentView(LoginRequiredMixin, View):

    def post(self, request):
        result, instance = CreateComment().execute({
            **(request.POST.dict() | {"user":request.user}),
        })
        if result == True:
            SendCommentNotification.execute({
                **(request.POST.dict() | {"user":request.user}),
            })
        return JsonResponse(CommentSerializer(instance).data)
    

class ViewThread(View):
    template_name = 'main_app/view_thread.html'

    def get(self, request, *args, **kwargs):
        thread, max_depth = ListThread.execute({
            **(self.kwargs | request.GET.dict()),
        })

        context = {
            "thread": thread,
            "max_depth": max_depth,
        }
        
        return render(request, self.template_name, context)