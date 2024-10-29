from django.forms import ModelForm
from models_app.models.photo_version.models import PhotoVersion

class PhotoVersionForm(ModelForm):
    
    def save(self, commit=True):
        return super().save(commit=commit)

    class Meta:
        model = PhotoVersion
        fields = ('title', 'description', 'pub_date', 'status', 'img')