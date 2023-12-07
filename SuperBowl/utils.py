from django.contrib.auth.models import User

def convert_email_to_username(email):
    try:
        user = User.objects.get(email=email)
        return user.username
    except User.DoesNotExist:
        return None
