from django.db import models
from django.db.models.signals import pre_save, post_save

from models_app.models.img_upl import uploaded_file_path, skip_saving_file, save_file
from ..meta_abstract.models import MetaAbstract

class Photo(MetaAbstract):
    # like_set
    # comment_set
    # photoversion_set
    user = models.ForeignKey('models_app.UserProfile', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField(null=True, default=None, blank=True)
    status = models.CharField(max_length=16)
    img = models.ImageField(upload_to=uploaded_file_path)


    def __str__(self):
        return f'{self.title}'

pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)