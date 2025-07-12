from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.views import LoginView
from service_objects.services import ServiceOutcome
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm

from models_app.admin.user_profile.forms import UserProfileForm, UserProfileLoginForm
from main_app.services import ListPhotos, GetUserGithubPFP, UpdateUserProfile, CreateUser, FormAccountLinkEmail, SetPasswordForUser
from models_app.admin.user_profile.forms import UserProfileCreationForm



from main_app.tokens import account_oauth_link_token_generator
from models_app.models import UserProfile
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

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
        is_oauth_user = outcome.result.get("is_oauth_user")
        user = outcome.result.get("user")
        form = outcome.result.get("form")
        
        if user and not is_oauth_user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("main_app:profile")
        
        if is_oauth_user:
            messages.warning(request, "We've sent verification link to your email.")
            outcome = ServiceOutcome(
                FormAccountLinkEmail,
                {
                    "user": user,
                    "domain": get_current_site(request).domain,
                    "protocol": "https" if request.is_secure() else "http"
                }
            )
            send_mail(
                subject="Adding password to OAuth account",
                message=outcome.result,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email]
            )
        return render(request, self.template_name, {"form": form})
        
    
class UserLoginView(LoginView):
    authentication_form = UserProfileLoginForm


class VerifyPasswordView(View):
    template_name = "registration/verify_password.html"

    def dispatch(self, request, *args, **kwargs):
        self.validlink = True
        try:
            self.user = self.get_user(kwargs['user_idb64'])
            token = kwargs['token']
            
            if not account_oauth_link_token_generator.check_token(self.user, token):
                self.validlink = False
            
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            self.validlink = False
            
        return super().dispatch(request, *args, **kwargs)

    def get_user(self, user_idb64):
        uid = force_str(urlsafe_base64_decode(user_idb64))
        return UserProfile.objects.get(pk=uid)
        
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": SetPasswordForm(None), "validlink": self.validlink})

    def post(self, request, *args, **kwargs):
        if not self.validlink:
            return self.get(request, args, kwargs)
        outcome = ServiceOutcome(
                SetPasswordForUser,
                {"user": self.user} | request.POST
        )
        user, form = outcome.result
        if user:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("main_app:profile")
        return render(request, self.template_name, {"form": form, "validlink": self.validlink})