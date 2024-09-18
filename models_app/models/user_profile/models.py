from django.contrib.auth.models import AbstractUser
from ..meta_abstract.models import MetaAbstract

class UserProfile(AbstractUser, MetaAbstract):
    pass