from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from main_app.services.photo.read import ReadPhotos
from main_app.services.photo.update import RecoverPhotoBeforeDeletion
from main_app.utils.mixins.utils import AuthorRequiredMixin
from models_app.models.photo.models import Photo

class RecoverPhoto(AuthorRequiredMixin, LoginRequiredMixin, View):
    model = Photo
    login_url = '/login/github'

    def get(self, request, *args, **kwargs):
        photo_obj = ReadPhotos.execute({'pk': kwargs['id']})
        recover_result = RecoverPhotoBeforeDeletion.execute({'photo': photo_obj})
        if recover_result is True:
            messages.success(request, 'Photo recovered successfully')
        else:
            messages.warning(request, "Couldn't recover photo. Check if photo status is To Be Deleted")
        return redirect('main_app:profile')
