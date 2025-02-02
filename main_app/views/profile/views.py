from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from models_app.admin.user_profile.forms import UserProfileForm
from ...services import ReadPhotos, ReadUserGithubPFP


class ProfileView(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/profile.html'

    def get(self, request, *args, **kwargs):
        context = {}

        photos = ReadPhotos().execute({
            "filter": {
                'user' : self.request.user,
            }
        })

        avatar_url = ReadUserGithubPFP().execute({
            'user_id' : self.request.user.id
        })
        page = request.GET.get('page', 1)
        context['photos_page'] = photos.get_page(page)
        context['avatar'] = avatar_url
        context['form'] = UserProfileForm(instance=self.request.user)

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('main_app:profile')
        
        return self.get(request, *args, **kwargs)