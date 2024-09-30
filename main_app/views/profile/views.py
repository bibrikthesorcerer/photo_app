from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from models_app.admin.user_profile.forms import UserProfileForm
from ...services import ReadPhotoByUserID, ReadUserGithubPFP


class ProfileView(LoginRequiredMixin, View):
    login_url='/login/github'
    redirect_field_name='/profile'
    template_name = 'main_app/profile.html'

    def get(self, request, *args, **kwargs):
        context = {}

        service_result = ReadPhotoByUserID.execute({
            'user_id' : self.request.user.id
        })

        avatar_result = ReadUserGithubPFP.execute({
            'user_id' : self.request.user.id
        })

        context['avatar'] = avatar_result
        context['photos'] = service_result
        context['form'] = UserProfileForm(instance=self.request.user)

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main_app:profile'))
        
        return self.get(request, *args, **kwargs)