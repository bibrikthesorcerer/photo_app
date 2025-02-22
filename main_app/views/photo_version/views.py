from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.services.photo import RetrievePhoto
from main_app.services.photo_version.read import ReadPhotoVersionsByPhotoID



class ViewPhotoVersions(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/view_photo_versions.html'

    def get(self, request, *args, **kwargs):
        photo_obj = RetrievePhoto.execute({**self.kwargs})
        versions = ReadPhotoVersionsByPhotoID.execute({**self.kwargs})
        return render(request, self.template_name, {'photo': photo_obj, 'versions': versions})