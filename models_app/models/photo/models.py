from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from models_app.models.base_model import BaseModel
from models_app.utils.img_save.utils import delete_photo_directory
from models_app.utils.img_save.utils import save_file
from models_app.utils.img_save.utils import skip_saving_file
from models_app.utils.img_save.utils import uploaded_file_path


class Photo(BaseModel):
    TO_BE_DELETED = "TBD"
    APPROVED = "APR"
    DENIED = "DEN"
    ON_MODERATION = "OM"

    STATUS_CHOICES = [
        (TO_BE_DELETED, "To Be Deleted"),
        (APPROVED, "Approved"),
        (DENIED, "Denied"),
        (ON_MODERATION, "On Moderation"),
    ]

    # like_set
    # comment_set
    # photoversion_set
    user = models.ForeignKey(
        "models_app.UserProfile", on_delete=models.SET_NULL, null=True
    )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    pub_date = models.DateTimeField(null=True, default=None, blank=True)
    status = models.CharField(
        max_length=16, choices=STATUS_CHOICES, default=ON_MODERATION
    )
    img = models.ImageField(upload_to=uploaded_file_path)
    img_thumbnail = ImageSpecField(
        source="img",
        processors=[ResizeToFit(300, 300)],
        format="JPEG",
        options={"quality": 60},
    )
    admin_thumbnail = ImageSpecField(
        source="img",
        processors=[ResizeToFit(100, 100)],
        format="JPEG",
        options={"quality": 60},
    )

    review_tickets = GenericRelation(
        "models_app.ReviewTicket", related_query_name="photo_version"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "photo"
        verbose_name_plural = "photos"
        db_table = "photos"


pre_save.connect(skip_saving_file, sender=Photo)
post_save.connect(save_file, sender=Photo)
post_delete.connect(delete_photo_directory, sender=Photo)
