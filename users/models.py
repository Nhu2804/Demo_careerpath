# users/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email là bắt buộc")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=150, unique=True, verbose_name="Tên đăng nhập"
    )
    email = models.EmailField(
        unique=True, verbose_name="Email"
    )
    first_name = models.CharField(
        max_length=30, blank=True, verbose_name="Họ"
    )
    last_name = models.CharField(
        max_length=30, blank=True, verbose_name="Tên"
    )
    is_active = models.BooleanField(
        default=True, verbose_name="Hoạt động"
    )
    is_staff = models.BooleanField(
        default=False, verbose_name="Quyền truy cập Admin"
    )
    date_joined = models.DateTimeField(
        auto_now_add=True, verbose_name="Ngày tham gia"
    )
    avatar = models.ImageField(
        upload_to='avatars/', default='avatars/default_avatar.png', verbose_name="Ảnh đại diện"
    )

    # THÊM TRƯỜNG NÀY (Để lưu link Google)
    avatar_url = models.URLField(max_length=500, blank=True, null=True)

    def get_avatar_url(self):
        # 1. Ưu tiên link từ Google
        if self.avatar_url:
            return self.avatar_url
        # 2. Nếu không có link Google thì dùng ảnh upload (nếu có)
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        # 3. Cuối cùng là ảnh mặc định (Để trong STATIC để không bị mất)
        return "/static/images/default_avatar.png"

    is_premium = models.BooleanField(
        default=False, verbose_name="Gói Premium"
    )
    premium_expiry = models.DateTimeField(
        null=True, blank=True, verbose_name="Hết hạn Premium"
    )

    # 👇 bổ sung 2 field này
    promoted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # hoặc 'self'
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='promoted_users',
        verbose_name='Người nâng quyền'
    )
    promoted_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Thời điểm nâng quyền'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Quản lý User"

    def __str__(self):
        return self.username

    # users/models.py (thêm dưới class CustomUser)
class SuperUserProxy(CustomUser):
    class Meta:
        proxy = True
        app_label = "users"  # ✅ Bổ sung dòng này
        verbose_name = "Quản lý Admin"
        verbose_name_plural = "Quản lý Admin"

class RegularUserProxy(CustomUser):
    class Meta:
        proxy = True
        app_label = "users"
        verbose_name = "Quản lý User"
        verbose_name_plural = "Quản lý User"




