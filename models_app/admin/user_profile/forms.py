from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from social_django.models import UserSocialAuth
from django import forms

from models_app.models import UserProfile


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for _, elem in self.fields.items():
            elem.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        self.user = super().save(commit)


class AdminUserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ("username", "email", "first_name", "last_name", "role")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, elem in self.fields.items():
            elem.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        return super().save(commit)


class UserProfileCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ("username", "password1", "password2")


class UserProfileLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                user = None

            try:
                social_auth = UserSocialAuth.objects.get(user=user)
            except UserSocialAuth.DoesNotExist:
                social_auth = None
            
            if user and social_auth:
                raise forms.ValidationError(
                    f"Your account was created using OAuth({social_auth.provider.capitalize()}). Login using {social_auth.provider.capitalize()}.",
                    code="social_account"
                )
        return super().clean()