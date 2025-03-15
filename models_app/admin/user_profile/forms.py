from django.forms import ModelForm

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
