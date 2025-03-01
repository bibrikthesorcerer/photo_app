from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.admin.photo.forms import PhotoForm
from models_app.models import UserProfile



class CreatePhoto(ServiceWithResult):
    user = ModelField(UserProfile)
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256)
    img = forms.ImageField()

    def _collect_form_data(self) -> dict[str, str]:
        post = {
            "title": self.cleaned_data.get("title"),
            "description": self.cleaned_data.get("description"),
            "img": self.cleaned_data.get("img")
        }
        files = {"img": self.cleaned_data.get("img")}
        return (post, files)
    
    def process(self) -> bool:
        user = self.cleaned_data.get("user")
        form = PhotoForm(*self._collect_form_data())
        self.result = False
        if form.is_valid():
            form.instance.user = user
            form.save()
            self.result = True
        return self.result