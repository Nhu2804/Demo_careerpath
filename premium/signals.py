# premium/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import PremiumSubscription

User = get_user_model()

@receiver(post_save)  # 👈 KHÔNG chỉ định sender để bắt cả proxy
def sync_subscription_from_user(sender, instance, **kwargs):
    """
    Khi admin/screen khác sửa CustomUser (kể cả proxy), chỉ tạo/cập nhật
    PremiumSubscription NẾU user thực sự có premium (is_premium=True hoặc có hạn).
    Không tạo cho user free.
    """
    # Chỉ xử lý cho model User thật (CustomUser) & proxy của nó
    if not isinstance(instance, User):
        return

    has_premium_flag = bool(instance.is_premium) or bool(instance.premium_expiry)
    sub = PremiumSubscription.objects.filter(user=instance).first()

    if not has_premium_flag:
        # User không còn premium => tắt subscription nếu đang có
        if sub and (sub.is_active or sub.subscription_end is not None):
            sub.is_active = False
            sub.subscription_end = None
            sub.save(update_fields=["is_active", "subscription_end"])
        return

    # Có premium: đảm bảo có subscription
    if not sub:
        sub = PremiumSubscription.objects.create(user=instance)
        sub.subscription_start = timezone.now()

    desired_active = bool(instance.is_premium)
    desired_end = instance.premium_expiry  # có thể None nếu premium “không thời hạn”

    changed = False
    if sub.is_active != desired_active:
        sub.is_active = desired_active
        changed = True
    if desired_active and sub.subscription_start is None:
        sub.subscription_start = timezone.now()
        changed = True
    if sub.subscription_end != desired_end:
        sub.subscription_end = desired_end
        changed = True

    if changed:
        sub.save(update_fields=["is_active", "subscription_start", "subscription_end"])


@receiver(post_save, sender=PremiumSubscription)
def sync_user_from_subscription(sender, instance: PremiumSubscription, **kwargs):
    """
    Đồng bộ ngược lại về CustomUser (tránh vòng lặp bằng cách chỉ set khi khác).
    """
    user = instance.user
    desired_is_premium = bool(instance.is_active)
    desired_expiry = instance.subscription_end

    update_fields = []
    if user.is_premium != desired_is_premium:
        user.is_premium = desired_is_premium
        update_fields.append("is_premium")
    if user.premium_expiry != desired_expiry:
        user.premium_expiry = desired_expiry
        update_fields.append("premium_expiry")

    if update_fields:
        user.save(update_fields=update_fields)
