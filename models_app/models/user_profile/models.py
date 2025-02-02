from django.contrib.auth.models import AbstractUser

from models_app.models.base_model import BaseModel

class UserProfile(AbstractUser, BaseModel):
    pass