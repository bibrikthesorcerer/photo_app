from django.db import models
from django.db.models.signals import pre_save, post_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from models_app.utils.img_save.utils import uploaded_file_path, skip_saving_file, save_file
from models_app.models.base_model import BaseModel

class Photo(BaseModel):
    TO_BE_DELETED = 'TBD'
    APPROVED = 'APR'
    DENIED = 'DEN'
    ON_MODERATION = 'OM'

    STATUS_CHOICES = [
        (TO_BE_DELETED, 'To Be Deleted'),
        (APPROVED, 'Approved'),
        (DENIED, 'Denied'),
        (ON_MODERATION, 'On Moderation'),
    ]

    # like_set
    # comment_set
    # photoversion_set
    user = models.ForeignKey('models_app.UserProfile', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField(null=True, default=None, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=ON_MODERATION)
    img = models.ImageField(upload_to=uploaded_file_path)
    img_thumbnail = ImageSpecField(source='img', processors=[ResizeToFit(300,300)], format='JPEG', options={'quality': 60})
    admin_thumbnail = ImageSpecField(source='img', processors=[ResizeToFit(100,100)], format='JPEG', options={'quality': 60})


    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = "photo"
        verbose_name_plural = "photos"
        db_table = "photos"

pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)