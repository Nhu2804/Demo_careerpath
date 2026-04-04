from django.urls import path
from . import views


app_name = 'premium'

urlpatterns = [
    path('', views.premium_home, name='premium_home'),
    path('renew/', views.renew_premium, name='renew_premium'),
    path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
    path('payos-webhook/', views.payos_webhook, name='payos_webhook'),  # Webhook từ PayOS
    path('check-payment/<str:order_id>/', views.check_payment, name='check_payment'),  # Để poll status
]
