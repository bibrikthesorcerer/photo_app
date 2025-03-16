from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from models_app.models import BaseModel
from models_app.models import Photo


class ReviewTicket(BaseModel):

    REVIEW_RESULT_CHOICES = [(Photo.APPROVED, "Approved"), (Photo.DENIED, "Denied")]
    result = models.CharField(max_length=16, choices=REVIEW_RESULT_CHOICES)
    commentary = models.TextField(null=True, blank=True)
    moderator = models.ForeignKey(
        "models_app.UserProfile", on_delete=models.SET_NULL, null=True
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reviewed_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"ReviewTicket for {self.reviewed_object}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["object_id", "content_type"], name="unique_review_photo"
            )
        ]
        verbose_name = "review_ticket"
        verbose_name_plural = "review_tickets"
        db_table = "review_tickets"
