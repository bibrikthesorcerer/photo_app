from django.forms import ModelForm
from models_app.models import Photo

class PhotoForm(ModelForm):   
    class Meta:
        model = Photo
        fields = ('title', 'description', 'img')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for _, elem in self.fields.items():
            elem.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        self.photo = super().save()  
        return self.photo