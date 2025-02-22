from django.contrib.auth.models import AbstractUser

from models_app.models.base_model import BaseModel


class UserProfile(AbstractUser, BaseModel):

    class Meta:
        verbose_name = "user_profile"
        verbose_name_plural = "user_profiles"
        db_table = "user_profiles"
