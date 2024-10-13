from django.forms import ModelForm
from models_app.models import Photo

class PhotoForm(ModelForm): 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for _, elem in self.fields.items():
            elem.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        return super().save(commit=commit)
    
    class Meta:
        model = Photo
        fields = ('title', 'description', 'img')