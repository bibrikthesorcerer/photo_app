from typing import Union
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.models import Comment, UserProfile, Photo
from models_app.admin.comment import CommentForm

from main_app.services.photo import ReadPhotos
from main_app.services.comment import RetrieveComment

class CreateComment(ServiceWithResult):
    photo_id = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    user = ModelField(UserProfile)
    text = forms.CharField()

    def process(self) -> tuple[bool, Union[Comment, None]]:
        parent = self._get_parent_comment()
        photo = parent.photo if parent else self._get_related_photo()
        data = {
            'parent': parent,
            'photo': photo,
            'user': self.cleaned_data['user'],
            'text': self.cleaned_data['text']
        }
        form = CommentForm(data)
        if form.is_valid():
            form.save()
            self.result = (True, form.instance,)
        else:
            self.result = (False, None,)
        
        return self.result
    
    def _get_parent_comment(self) -> Comment:
        parent_id = self.cleaned_data['parent_id']
        if not parent_id:
            return None
        return RetrieveComment().execute({'pk': parent_id})
    
    def _get_related_photo(self) -> Photo:
        photo_id = self.cleaned_data['photo_id']
        return ReadPhotos.execute({'pk': photo_id})