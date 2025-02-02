from django.forms import ModelForm, ValidationError
from models_app.models import Comment

class CommentForm(ModelForm): 

    def clean_parent(self):
        parent = self.cleaned_data['parent']
        photo = self.cleaned_data['photo']
        if photo != parent.photo:
            raise ValidationError("Photo of child must match photo of parent")
        return parent

    class Meta:
        model = Comment
        exclude = ['deleted_at']