from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class PremiumSubscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)

    def activate_subscription(self, months=1):
        now = timezone.now()
        self.subscription_start = now
        self.subscription_end = now + timedelta(days=30 * months)
        self.is_active = True
        self.save()

    def check_status(self):
        now = timezone.now()
        if self.subscription_end and now > self.subscription_end:
            self.is_active = False
            self.save()
        return self.is_active

    @property
    def days_left(self):
        now = timezone.now()
        if self.subscription_end:
            delta = self.subscription_end - now
            return max(delta.days, 0)
        return 0

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)
    amount = models.IntegerField()
    months = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_link_id = models.CharField(max_length=100, blank=True, null=True)