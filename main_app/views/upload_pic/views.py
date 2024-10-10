from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from main_app.services.photo.process import CreatePhotoThumbnailJPEG
from models_app.admin.photo.forms import PhotoForm


class UploadPhoto(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/upload_pic.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': PhotoForm})
    
    def post(self, request, *args, **kwargs):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Photo uploaded successfully')

            CreatePhotoThumbnailJPEG.execute({'path': photo.img})

            return HttpResponseRedirect(reverse('main_app:profile'))
        
        return render(request, self.template_name, {'form': form})