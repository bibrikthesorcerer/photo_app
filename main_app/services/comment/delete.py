from service_objects.services import ServiceWithResult
from django import forms

from models_app.models import Comment
from main_app.services.comment import RetrieveComment


class DeleteComment(ServiceWithResult):
    comment_id = forms.IntegerField()

    def process(self) -> tuple[Comment, bool]:
        comment_id = self.cleaned_data.get('comment_id')
        comment_obj = RetrieveComment.execute({"pk": comment_id})
        if comment_obj.children.all():
            comment_obj.text = 'Comment was deleted by user'
            comment_obj.save()
            self.result = (comment_obj, False)
        else:
            comment_obj = Comment.objects.filter(id=comment_id).delete().first()
            self.result = (comment_obj, True)
        
        return self.result