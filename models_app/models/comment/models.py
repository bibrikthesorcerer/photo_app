from django.db import models

from models_app.models.base_model import BaseModel, SoftDelMixin

class Comment(BaseModel, SoftDelMixin):
    user = models.ForeignKey('models_app.UserProfile', on_delete=models.CASCADE)
    photo = models.ForeignKey('models_app.Photo', on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, related_name='children', null=True, default=None, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text}'
    
    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        db_table = "comments"