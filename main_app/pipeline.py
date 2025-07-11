from models_app.models import UserProfile

def get_or_create_user(strategy, details, backend, user=None, *args, **kwargs):
    username = details.get("username", kwargs.get("username"))
    user, is_new = UserProfile.objects.get_or_create(username=username, defaults=details)
    return {"is_new": bool(is_new), "user": user}