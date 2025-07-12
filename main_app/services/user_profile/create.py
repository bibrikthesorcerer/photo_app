from service_objects.services import ServiceWithResult
from django import forms

from models_app.admin.user_profile.forms import UserProfileCreationForm
from models_app.models import UserProfile


class CreateUser(ServiceWithResult):
    username = forms.CharField()
    email = forms.EmailField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def process(self):
        self.result = self._create_user()
        return self
    
    def _create_user(self) -> dict:
        self.form = UserProfileCreationForm(self.cleaned_data)
        self.user = None
        is_oauth_user = self._is_oauth_user()
        if self.form.is_valid():
                self.user = self.form.save(),
        return {
            "user": self.user,
            "form": self.form,
            "is_oauth_user": is_oauth_user
        }
    
    def _is_oauth_user(self) -> bool:
        try:
            self.user = UserProfile.objects.get(email=self.cleaned_data.get("email"))
            if self.user.has_usable_password():
                self.form.add_error('email', 'User with this email already exists')
                return False
            else:
                self.form.add_error("email", "Account with given email exists and was created using OAuth.")
                return True
        except UserProfile.DoesNotExist:
            return False