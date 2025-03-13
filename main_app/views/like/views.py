from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict

from main_app.services import UpdateOrCreateLike, DeleteLike
from main_app.services import RetrievePhoto
from main_app.permissions import PlainUserOnly


class CreateLike(PlainUserOnly, View):
    login_url='/login/github'

    def post(self, request):
        photo_obj = RetrievePhoto.execute({**request.POST.dict()})
        
        like_obj = UpdateOrCreateLike.execute({
            'photo': photo_obj,
            'user': request.user,
        })

        return JsonResponse(model_to_dict(like_obj))


class RemoveLike(PlainUserOnly, View):
    login_url='/login/github'

    def post(self, request):
        like_obj = DeleteLike.execute({
            **(request.POST.dict() | {'user_id': request.user.id})
        })
        
        return JsonResponse(model_to_dict(like_obj))