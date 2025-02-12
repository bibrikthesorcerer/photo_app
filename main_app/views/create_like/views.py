from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict

from main_app.services.like import UpdateOrCreateLike
from main_app.services.photo import ReadPhotos

class CreateLike(LoginRequiredMixin, View):
    login_url='/login/github'

    def post(self, request):
        photo_id = request.POST['photo_id']
        photo_obj = ReadPhotos().execute({'pk': photo_id})
        
        like_obj = UpdateOrCreateLike().execute({
            'photo': photo_obj,
            'user': request.user,
        })

        return JsonResponse(model_to_dict(like_obj))