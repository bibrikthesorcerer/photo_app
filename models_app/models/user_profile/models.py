from django.contrib.auth.models import AbstractUser
from django.db import models

from models_app.models.base_model import BaseModel


class UserProfile(AbstractUser, BaseModel):
    ROLE_USER = "USR"
    ROLE_MOD = "MOD"
    ROLE_ADMIN = "ADM"
    ROLES = [
        [ROLE_USER, "User"],
        [ROLE_MOD, "Moderator"],
        [ROLE_ADMIN, "Administrator"],
    ]

    role = models.CharField(choices=ROLES, default=ROLE_USER)

    class Meta:
        verbose_name = "user_profile"
        verbose_name_plural = "user_profiles"
        db_table = "user_profiles"
        constraints = [
            models.UniqueConstraint(fields=["email"], name="unique_email_for_user")
        ]
