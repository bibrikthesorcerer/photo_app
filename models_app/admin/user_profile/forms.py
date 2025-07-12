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
        if self.instance.pk:
            self.fields['username'].disabled = True
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
        if self.instance.pk:
            self.fields['username'].disabled = True
        for _, elem in self.fields.items():
            elem.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        return super().save(commit)


class UserProfileCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="This email will be used to reset your password if needed. No spam, we promise.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user

    class Meta:
        model = UserProfile
        fields = ("username", "email", "password1", "password2")


class UserProfileLoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            try:
                user = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                user = None
            
            if user and not user.has_usable_password():
                raise forms.ValidationError(
                    f"Your account probably was created using OAuth and you have not set password yet. Login using OAuth or set password by signing-up with your email again.",
                    code="social_account"
                )
        return super().clean()