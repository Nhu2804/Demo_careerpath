import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Careerpath.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = os.getenv("ADMIN_USERNAME", "admin")
email = os.getenv("ADMIN_EMAIL", "admin@gmail.com")
password = os.getenv("ADMIN_PASSWORD")

if not password:
    print("ADMIN_PASSWORD is not set.")
else:
    if User.objects.filter(username=username).exists():
        print(f"Admin '{username}' already exists.")
    else:
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"Admin '{username}' created successfully.")