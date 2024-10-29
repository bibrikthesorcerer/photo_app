from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from main_app.services.photo.process import CreatePhotoThumbnailJPEG
from models_app.admin.photo.forms import PhotoForm


class UploadPhoto(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/upload_photo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': PhotoForm})
    
    def post(self, request, *args, **kwargs):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # вынести в сервис
            photo_obj = form.save(commit=False)
            photo_obj.user = request.user
            # ======
            photo_obj.save()
            messages.success(request, 'Photo uploaded successfully')

            CreatePhotoThumbnailJPEG.execute({'path': photo_obj.img})

            return redirect('main_app:profile')
        
        return render(request, self.template_name, {'form': form})