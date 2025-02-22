from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from models_app.admin.user_profile.forms import UserProfileForm
from main_app.services import ListPhotos, GetUserGithubPFP


class UserProfileView(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/profile.html'

    def get(self, request, *args, **kwargs):
        photos = ListPhotos().execute({
            **(request.GET.dict() | {"author": request.user})
        })

        avatar_url = GetUserGithubPFP().execute({
            "user" : request.user
        })

        context = {
            'params': f'per_page={photos.paginator.per_page}',
            'photos_page': photos,
            'avatar' : avatar_url,
            'form': UserProfileForm(instance=request.user),
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('main_app:profile')
        
        return self.get(request, *args, **kwargs)