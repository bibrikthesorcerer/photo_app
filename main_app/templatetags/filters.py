from django import template
from models_app.models.photo.models import Photo
from models_app.models.user_profile.models import UserProfile
import os.path

register = template.Library()
    
@register.filter()
def is_liked(value: Photo, req_user: UserProfile) -> bool:
    if isinstance(value, Photo):
        likes = value.like_set.all()
        return len(likes.filter(user=req_user, deleted_at=None))
    
@register.filter()
def get_thumbnail(value: str) -> str:
    filepath, extension = os.path.splitext(value)
    return f'{filepath}_thumbnail.jpeg'