from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django import forms

from models_app.models import Comment


class UpdateCommentText(ServiceWithResult):
    comment = ModelField(Comment)
    text = forms.CharField(max_length=256)

    def process(self):
        comment = self.cleaned_data.get("comment")
        comment.text = self.cleaned_data.get("text")
        comment.save()
        self.result = comment
        return self
    

class DeleteComment(ServiceWithResult):
    comment = ModelField(Comment)

    def process(self) -> tuple[Comment, bool]:
        comment = self.cleaned_data.get("comment")
        is_deleted = False
        if comment.children.all():
            comment.text = 'DELETED'
            comment.save()
        else:
            is_deleted = True
        comment = Comment.objects.filter(id=comment.id).delete().first()
        self.result = (comment, is_deleted)
        return self