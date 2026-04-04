from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PremiumSubscription, Transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse

import json
import random
import base64
from io import BytesIO
from django.urls import reverse
import qrcode
from payos import PayOS, ItemData, PaymentData
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import logging

logger = logging.getLogger(__name__)

from django.conf import settings

if settings.PAYOS_CLIENT_ID:
    payOS = PayOS(
        settings.PAYOS_CLIENT_ID,
        settings.PAYOS_API_KEY,
        settings.PAYOS_CHECKSUM_KEY
    )
else:
    payOS = None

User = get_user_model()

def send_payment_confirmation_email(user, months, amount):
    subject = 'Xác Nhận Thanh Toán Premium - CareerPath'
    context = {
        'user': user,
        'months': months,
        'amount': amount,
        'end_date': timezone.now() + timezone.timedelta(days=30 * months),
    }
    message = render_to_string('email_payment_confirmation.html', context)
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
    )

def premium_home(request):
    user = request.user if request.user.is_authenticated else None
    subscription = None
    subscription_active = False
    days_left = 0

    if user:
        subscription = PremiumSubscription.objects.filter(user=user).first()
        if subscription:
            subscription_active = subscription.check_status()  # <-- dùng check_status
            if subscription.subscription_end:
                delta = subscription.subscription_end - timezone.now()
                days_left = max(delta.days, 0)

    context = {
        "subscription": subscription,
        "subscription_active": subscription_active,
        "days_left": days_left,
        "user": user,
    }
    return render(request, 'premium.html', context)


def get_price(months: int) -> int:
    try:
        return int(settings.PREMIUM_PRICING[int(months)])
    except Exception:
        # months không hợp lệ -> chặn
        raise ValueError("Gói không hợp lệ")
    

def compute_plans(pricing):
    base = pricing.get(1)
    plans = []
    for m, v in pricing.items():
        if m == 1 or not base:
            saving_pct = 0
        else:
            original = base * m
            saving_pct = max(0, round((original - v) / original * 100))
        plans.append({'months': m, 'price': v, 'saving_pct': saving_pct})
    # sort theo số tháng
    plans.sort(key=lambda x: x['months'])
    return plans

    
@login_required
def renew_premium(request):
    user = request.user

    # Chỉ đọc: không tạo mới ở đây
    subscription = PremiumSubscription.objects.filter(user=user).first()

    # Mặc định
    is_first_time = True
    is_expired = False

    if subscription:
        subscription.check_status()
        # Nếu chưa từng kích hoạt -> lần đầu
        is_first_time = (subscription.subscription_start is None)
        # Nếu từng có start nhưng hiện không active -> hết hạn / tạm dừng
        is_expired = (subscription.subscription_start is not None) and (not subscription.is_active)

    # Tiêu đề/trợ ngôn ngữ
    if is_first_time:
        page_title = "Đăng ký Premium"
        hero_subtitle = "Điền thông tin để bắt đầu trải nghiệm Premium với đầy đủ tính năng nâng cao."
        cta_label = "Tiếp tục thanh toán"
    else:
        page_title = "Gia hạn Premium" if is_expired else "Gia hạn/Quản lý Premium"
        hero_subtitle = (
            "Gói Premium của bạn đã hết hạn. Vui lòng gia hạn để tiếp tục sử dụng đầy đủ tính năng."
            if is_expired else
            "Cập nhật thông tin để tiếp tục quản lý gói Premium."
        )
        cta_label = "Tiếp tục thanh toán"

    if request.method == "POST":      
        try:
            months = int(request.POST.get('months', 1))
            amount = get_price(months)  # ✅ đồng bộ với UI
        except ValueError:
            return HttpResponseBadRequest("Gói không hợp lệ")

        context = {
            'amount': amount,
            'months': months,
            'user': user,
        }
        return render(request, 'premium_payment_qr.html', context)
    plans = compute_plans(settings.PREMIUM_PRICING)
    return render(
        request,
        'renew_premium.html',
        {
            "user": user,
            "subscription": subscription,  # có thể là None -> template cần if-check
            "is_first_time": is_first_time,
            "is_expired": is_expired,
            "page_title": page_title,
            "hero_subtitle": hero_subtitle,
            "cta_label": cta_label,
            "pricing": settings.PREMIUM_PRICING, 
            "plans": plans,
        }
    )

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            months_raw = data.get('months', None)
            months = int(months_raw)
            amount = get_price(months)
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Gói không hợp lệ'}, status=400)

        order_code = random.randint(100000000, 999999999)
        transaction = Transaction.objects.create(
            user=request.user,
            order_id=str(order_code),
            amount=amount,
            months=months,
            status='pending'
        )
        item = ItemData(name=f"Gói Premium {months} tháng", quantity=1, price=amount)
        payment_data = PaymentData(
            orderCode=order_code,
            amount=amount,
            description=f"CP {str(order_code)}",  # Nội dung chuyển khoản ngắn gọn
            items=[item],
            returnUrl=request.build_absolute_uri(reverse('premium:premium_home')),
            cancelUrl=request.build_absolute_uri(reverse('premium:premium_home'))
        )

        try:
            link_response = payOS.createPaymentLink(payment_data)
            transaction.payment_link_id = link_response.paymentLinkId  # Lưu ID
            transaction.save()

            # Tạo QR code base64 từ qrCode string
            qr_str = link_response.qrCode
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_str)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffered = BytesIO()
            img.save(buffered)
            qr_base64 = base64.b64encode(buffered.getvalue()).decode('ascii')

            # Bank info (bin to name, thêm nhiều bank nếu cần)
            bin_code = link_response.bin
            bank_names = {
                '970418': 'BIDV',  
                # Thêm bin code khác
            }
            bank_name = bank_names.get(bin_code, 'Ngân hàng liên kết')

            return JsonResponse({
                'status': 'success',
                'order_id': transaction.order_id,
                'qr_code': qr_base64,
                'bank_name': bank_name,
                'account_number': link_response.accountNumber,
                'account_name': link_response.accountName,
                'description': payment_data.description
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return HttpResponseBadRequest()

@csrf_exempt
def payos_webhook(request):
    if request.method == 'POST':
        try:
            raw_body = request.body.decode('utf-8')
            logger.info("Webhook RAW body: %s", raw_body)   # log JSON gốc

            body = json.loads(raw_body)
            logger.info("Webhook parsed JSON: %s", body)

            verified_data = payOS.verifyPaymentWebhookData(body)
            logger.info("Webhook verified: %s", verified_data)

            order_code = str(verified_data.orderCode) 
            status_code = str(verified_data.code)    
            transaction = get_object_or_404(Transaction, order_id=order_code)

            if transaction.status == 'pending':
                if status_code == '00':
                    subscription, _ = PremiumSubscription.objects.get_or_create(user=transaction.user)
                    subscription.activate_subscription(months=transaction.months)
                    transaction.status = 'completed'
                    transaction.save()
                    send_payment_confirmation_email(
                        transaction.user,
                        transaction.months,
                        transaction.amount
                    )
                    logger.info("Payment success for order %s", order_code)
                else:
                    transaction.status = 'failed'
                    transaction.save()
                    logger.warning("Payment failed for order %s", order_code)

            return JsonResponse({'success': True})

        except Exception as e:
            logger.error("Webhook error: %s", str(e), exc_info=True)
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return HttpResponseBadRequest()

@login_required
def check_payment(request, order_id):
    transaction = get_object_or_404(Transaction, order_id=order_id, user=request.user)
    return JsonResponse({'status': transaction.status})

def premium_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        subscription = PremiumSubscription.objects.filter(user=request.user).first()
        if not subscription or not subscription.check_status():
            return redirect('premium:renew_premium')
        return view_func(request, *args, **kwargs)
    return wrapper