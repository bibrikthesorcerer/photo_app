from models_app.models import UserProfile


def get_or_create_user(strategy, details, backend, user=None, *args, **kwargs):
    email = details.get("email", kwargs.get("email"))
    username = details.get("username", kwargs.get("username"))
    first_name = details.get("first_name", kwargs.get("first_name"))
    last_name = details.get("last_name", kwargs.get("last_name"))
    user_details = {
        "email": email,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
    }
    user, is_new = UserProfile.objects.get_or_create(email=email, defaults=user_details)
    if is_new:
        user.set_unusable_password()
        user.save()
    return {"is_new": bool(is_new), "user": user}

