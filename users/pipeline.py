from social_core.exceptions import AuthException
from social_core.backends.google import GoogleOAuth2
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import requests

User = get_user_model()

def save_avatar_from_google(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        url = response.get('picture')
        if url and user:
            user.avatar_external = url
            user.save()

def associate_by_email(backend, details, user=None, *args, **kwargs):
    if user: return None
    email = details.get('email')
    if email:
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            return {'user': User.objects.get(email=email)}
        except User.DoesNotExist:
            return None