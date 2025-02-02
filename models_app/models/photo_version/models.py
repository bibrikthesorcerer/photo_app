from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from models_app.models.base_model import BaseModel

class PhotoVersion(BaseModel):
    photo = models.ForeignKey('models_app.Photo', on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField(null=True, default=None, blank=True)
    status = models.CharField(max_length=16)
    img = models.ImageField()
    img_thumbnail = ImageSpecField(source='img', processors=[ResizeToFit(300,300)], format='JPEG', options={'quality': 60})
    admin_thumbnail = ImageSpecField(source='img', processors=[ResizeToFit(100,100)], format='JPEG', options={'quality': 60})


    def __str__(self):
        return f"{self.photo.title} - version"
    
    class Meta:
        verbose_name = "photo_version"
        verbose_name_plural = "photo_versions"
        db_table = "photo_versions"