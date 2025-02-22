from django.db import models

from models_app.models.base_model import BaseModel
from models_app.models.base_model import SoftDelMixin


class Like(BaseModel, SoftDelMixin):
    photo = models.ForeignKey("models_app.Photo", on_delete=models.CASCADE)
    user = models.ForeignKey("models_app.UserProfile", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} on {self.photo}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["photo", "user"], name="unique_photo_user")
        ]
        verbose_name = "like"
        verbose_name_plural = "likes"
        db_table = "likes"
