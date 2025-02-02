from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from main_app.utils.mixins.utils import AuthorRequiredMixin
from main_app.services.photo.read import ReadPhotos
from main_app.services.photo_version.read import ReadPhotoVersionsByPhotoID
from models_app.models.photo.models import Photo



class ViewPhotoVersions(AuthorRequiredMixin, LoginRequiredMixin, View):
    model = Photo
    login_url='/login/github'
    template_name = 'main_app/view_photo_versions.html'

    def get(self, request, *args, **kwargs):
        photo_obj = ReadPhotos.execute({'pk': kwargs['id']})
        versions = ReadPhotoVersionsByPhotoID.execute({'photo_id': kwargs['id']})
        return render(request, self.template_name, {'photo': photo_obj, 'versions': versions})