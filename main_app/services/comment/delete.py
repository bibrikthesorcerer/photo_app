from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Comment
from main_app.services.comment import RetrieveComment


class DeleteComment(ServiceWithResult):
    comment_id = forms.IntegerField()

    def process(self) -> tuple[Comment, bool]:
        comment_obj = RetrieveComment.execute({**self.cleaned_data})
        is_deleted = False
        if comment_obj.children.all():
            comment_obj.text = 'DELETED'
            comment_obj.save()
        else:
            is_deleted = True
        comment_obj = Comment.objects.filter(id=comment_obj.id).delete().first()
        self.result = (comment_obj, is_deleted)
        return self.result