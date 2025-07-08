from service_objects.services import ServiceWithResult
from django import forms
from models_app.admin.user_profile.forms import UserProfileCreationForm


class CreateUser(ServiceWithResult):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    def process(self):
        self.result = self._create_user()
        return self
    
    def _create_user(self):
        self.form = UserProfileCreationForm(self.cleaned_data)
        if self.form.is_valid():
            return (self.form.save(), self.form)
        return (None, self.form)
            