from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Comment
from main_app.services.comment import RetrieveComment


class DeleteComment(ServiceWithResult):
    comment_id = forms.IntegerField()

    def process(self) -> tuple[Comment, bool]:
        comment_id = self.cleaned_data.get('comment_id')
        comment_obj = RetrieveComment.execute({"pk": comment_id})
        is_deleted = False
        if comment_obj.children.all():
            comment_obj.text = 'DELETED'
            comment_obj.save()
        else:
            is_deleted = True
        comment_obj = Comment.objects.filter(id=comment_id).delete().first()
        self.result = (comment_obj, is_deleted)
        return self.result