from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from main_app.utils.mixins.utils import AuthorRequiredMixin
from main_app.services.photo.read import ReadPhotos
from main_app.services.photo_version.create import CreatePhotoVersion
from models_app.admin.photo.forms import PhotoForm
from models_app.models.photo.models import Photo


class EditPhoto(LoginRequiredMixin,AuthorRequiredMixin, View):
    model = Photo
    login_url='/login/github'
    template_name = 'main_app/edit_photo.html'

    def get_editing_photo(self):
        return ReadPhotos().execute({
            'pk': self.kwargs['id']
            })

    def get(self, request, *args, **kwargs):
        photo_obj = self.get_editing_photo()
        form = PhotoForm(instance=photo_obj)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        photo_obj = self.get_editing_photo()
        form = PhotoForm(request.POST, request.FILES, instance=photo_obj)
        
        if form.is_valid():
            CreatePhotoVersion.execute({'photo_id': photo_obj.id})
            photo_obj = form.save()
            # CreatePhotoThumbnailJPEG.execute({'path': photo_obj.img})
            messages.success(request, 'Photo uploaded successfully')
            return redirect('main_app:profile')
        
        return render(request, self.template_name, {'form': form})