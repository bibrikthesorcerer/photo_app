from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from main_app.services.photo.read import ReadPhotos
from main_app.utils.mixins.utils import AuthorRequiredMixin
from main_app.services.photo.update import SchedulePhotoDeletion
from models_app.models.photo.models import Photo

class DeletePhoto(AuthorRequiredMixin, LoginRequiredMixin, View):
    model = Photo
    login_url = '/login/github'

    def get(self, request, *args, **kwargs):
        photo_obj = ReadPhotos.execute({'pk': kwargs['id']})
        sched_result = SchedulePhotoDeletion.execute({'photo': photo_obj})
        if sched_result is True:
            messages.success(request, 'Photo scheduled to be deleted successfully')
        else:
            messages.warning(request, "Couldn't schedule deletion of photo")
        return redirect('main_app:profile')
