from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.models import UserProfile

class UpdateUserProfile(ServiceWithResult):
    user = ModelField(UserProfile)
    username = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    # email = forms.EmailField(required=False)

    def process(self) -> UserProfile:
        self.result = self._update_user_fields()
        return self.result
    
    def _update_user_fields(self) -> UserProfile:
        user = self.cleaned_data.get('user')
        for attr, value in self.cleaned_data.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
        user.save()
        return user