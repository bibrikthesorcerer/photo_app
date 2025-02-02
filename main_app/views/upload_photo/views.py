from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from models_app.admin.photo.forms import PhotoForm


class UploadPhoto(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/upload_photo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': PhotoForm})
    
    def post(self, request, *args, **kwargs):
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request, 'Photo uploaded successfully')
            return redirect('main_app:profile')
        
        return render(request, self.template_name, {'form': form})