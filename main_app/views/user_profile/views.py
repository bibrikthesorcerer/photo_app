from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from service_objects.services import ServiceOutcome
from django.contrib.auth import login

from models_app.admin.user_profile.forms import UserProfileForm, UserProfileLoginForm
from main_app.services import ListPhotos, GetUserGithubPFP, UpdateUserProfile, CreateUser
from models_app.admin.user_profile.forms import UserProfileCreationForm


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
        is_success = UpdateUserProfile.execute({
            **(request.POST.dict() | {"user": request.user})
        })
        if is_success:
            messages.success(request, 'Your profile has been updated successfully')
            return redirect('main_app:profile')
        
        return self.get(request, *args, **kwargs)
    

class UserSignupView(View):
    template_name='registration/signup.html'

    def get(self, request):
        return render(request, self.template_name, {"form": UserProfileCreationForm()})

    def post(self, request):
        outcome = ServiceOutcome(
            CreateUser,
            request.POST
        )
        user, form = outcome.result
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("main_app:profile")
        else:
            return render(request, self.template_name, {"form": form})
        
    
class UserLoginView(LoginView):
    authentication_form = UserProfileLoginForm
