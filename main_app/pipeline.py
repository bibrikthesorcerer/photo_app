from models_app.models import UserProfile

def get_or_create_user(strategy, details, backend, user=None, *args, **kwargs):
    email = details.get("email", kwargs.get("email"))
    user, is_new = UserProfile.objects.get_or_create(email=email, defaults=details)
    if is_new:
        user.set_unusable_password()
        user.save()
    return {"is_new": bool(is_new), "user": user}