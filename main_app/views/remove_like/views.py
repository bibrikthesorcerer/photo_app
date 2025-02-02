from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict

from main_app.services.like import SoftDeleteLike

class RemoveLike(LoginRequiredMixin, View):
    login_url='/login/github'

    def post(self, request):
        like_obj = SoftDeleteLike.execute({
            'photo_id': request.POST['photo_id'], 
            'user_id': request.user.id
            })
        data = model_to_dict(like_obj)
        return JsonResponse(data)