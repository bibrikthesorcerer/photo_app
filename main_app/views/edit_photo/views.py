from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from main_app.services.mixins import AuthorRequiredMixin
from main_app.services.photo.process import CreatePhotoThumbnailJPEG
from main_app.services.photo.read import ReadPhotoByID
from main_app.services.photo_version.create import CreatePhotoVersion
from models_app.admin.photo.forms import PhotoForm
from models_app.models.photo.models import Photo


class EditPhoto(LoginRequiredMixin,AuthorRequiredMixin, View):
    model = Photo
    login_url='/login/github'
    template_name = 'main_app/edit_photo.html'

    def get(self, request, *args, **kwargs):
        photo_obj = ReadPhotoByID().execute({'photo_id': self.kwargs['id']})
        form = PhotoForm(instance=photo_obj)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        photo_obj = ReadPhotoByID().execute({'photo_id': self.kwargs['id']})
        form = PhotoForm(request.POST, request.FILES, instance=photo_obj)
        
        if form.is_valid():
            CreatePhotoVersion.execute({'photo_id': photo_obj.id})
            photo_obj = form.save()
            CreatePhotoThumbnailJPEG.execute({'path': photo_obj.img})
            messages.success(request, 'Photo uploaded successfully')
            return redirect('main_app:profile')
        
        return render(request, self.template_name, {'form': form})