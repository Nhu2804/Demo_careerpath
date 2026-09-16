from social_core.exceptions import AuthException
from social_core.backends.google import GoogleOAuth2
from django.contrib.auth import get_user_model


User = get_user_model()

def associate_by_email(backend, details, user=None, *args, **kwargs):
    """
    Tự động liên kết tài khoản Google OAuth với user đã tồn tại bằng email.
    """
    if user:
        return None

    email = details.get('email')
    if email:
        try:
            user = User.objects.get(email=email)
            return {'user': user}
        except User.DoesNotExist:
            return None

def save_avatar_from_google(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    if not user:
        return

    avatar_url = response.get('picture')
    if avatar_url and user.google_avatar_url != avatar_url:
        user.google_avatar_url = avatar_url
        user.save(update_fields=['google_avatar_url'])