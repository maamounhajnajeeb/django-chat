from django.contrib.auth import get_user_model

Users = get_user_model()

def activate_user(user) -> bool:
    user.is_active = True
    user.save()

    return True
