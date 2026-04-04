from datetime import timedelta
from django.utils import timezone
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib import admin as django_admin

from users.models import CustomUser
from quiz_highschool.models import QuizHighschool
from quiz_university.models import QuizUniversity
import json
from datetime import datetime, time, timedelta
from django.utils import timezone

from django.contrib.auth import get_user_model
from premium.models import PremiumSubscription, Transaction
from django.db.models import Count, OuterRef, Subquery 
from django.db.models import Sum

User = get_user_model()

@staff_member_required
def admin_dashboard(request):
    admin_ctx = django_admin.site.each_context(request)

    now = timezone.now()
    start_7 = now - timedelta(days=7)

    total_users   = CustomUser.objects.count()
    admin_count   = CustomUser.objects.filter(is_staff=True).count()
    superadmin_count = CustomUser.objects.filter(is_superuser=True).count()
    signups_7d    = CustomUser.objects.filter(date_joined__gte=start_7).count()

    hs_user_ids   = set(QuizHighschool.objects.values_list('user_id', flat=True).distinct())
    uni_user_ids  = set(QuizUniversity.objects.values_list('user_id', flat=True).distinct())
    both_users    = hs_user_ids & uni_user_ids
    hs_only_users = hs_user_ids - uni_user_ids
    uni_only_users= uni_user_ids - hs_user_ids
    quiz_users    = len(hs_user_ids | uni_user_ids)
    no_quiz       = max(total_users - quiz_users, 0)
    quiz_rate     = round((quiz_users / total_users) * 100, 1) if total_users else 0.0

    # ===== Đăng ký 7 ngày (đếm theo ngày) =====
    labels_7, signups_series_7 = [], []
    tz = timezone.get_current_timezone()
    for i in range(6, -1, -1):
        day = (now - timedelta(days=i)).date()
        labels_7.append(day.strftime("%d/%m"))
        start = timezone.make_aware(datetime.combine(day, time.min), tz)
        end   = start + timedelta(days=1)
        signups_series_7.append(
            CustomUser.objects.filter(date_joined__gte=start,
                                      date_joined__lt=end).count()
        )

    quiz_labels = ["Học sinh", "Sinh viên", "Cả hai", "Chưa làm"]
    quiz_values = [len(hs_only_users), len(uni_only_users), len(both_users), no_quiz]

    # ===================== PREMIUM KPI & PHÂN BỔ GÓI =====================
    # Premium đang hoạt động (an toàn theo thời gian)
    premium_active = PremiumSubscription.objects.filter(
        is_active=True, subscription_end__gt=now
    ).count()

    # Kích hoạt Premium trong 7 ngày gần đây
    premium_activations_7d = PremiumSubscription.objects.filter(
        subscription_start__gte=start_7
    ).count()
    
     # ==== DOANH THU & ĐƠN HÀNG THÁNG NÀY (gắn với Premium/Transaction) ====
    tx_month = Transaction.objects.filter(
        created_at__year=now.year,
        created_at__month=now.month
    )

    # Tổng đơn hàng tháng này (mọi trạng thái)
    total_orders_month = tx_month.count()

    # Doanh thu tháng này (chỉ tính các giao dịch "completed")
    revenue_month = tx_month.filter(status='completed').aggregate(
        s=Sum('amount')
    )['s'] or 0

    # Phân bổ trạng thái đơn hàng để vẽ donut
    status_rows = tx_month.values('status').annotate(c=Count('id'))
    status_map = {'completed': 0, 'pending': 0, 'failed': 0}
    for r in status_rows:
        status_map[r['status']] = r['c']

    order_status_labels = ['Đã thanh toán', 'Chờ thanh toán', 'Thất bại']
    order_status_values = [
        status_map['completed'],
        status_map['pending'],
        status_map['failed'],
    ]

    # Thu theo kênh thanh toán (tạm thời 1 kênh Website)
    payment_channels = [
        {'name': 'CareerPath website', 'amount': revenue_month}
    ]

    last_months_sq = Transaction.objects.filter(
        user=OuterRef('pk'),
        status='completed'
    ).order_by('-created_at').values('months')[:1]

    latest_plan_rows = User.objects.annotate(
        latest_months=Subquery(last_months_sq)
    ).values('latest_months').exclude(latest_months__isnull=True).annotate(
        c=Count('pk')
    ).order_by('latest_months')

    plan_labels, plan_values = [], []
    for row in latest_plan_rows:
        m = row['latest_months']
        plan_labels.append(f"{m} tháng")
        plan_values.append(row['c'])

    # ===================== CTX =====================
    ctx = {
        "total_users": total_users,
        "admin_count": admin_count,
        "superadmin_count": superadmin_count,
        "signups_7d": signups_7d,
        "quiz_users": quiz_users,
        "quiz_rate": quiz_rate,
        "labels_7": labels_7,
        "signups_series_7": signups_series_7,
        "quiz_labels": quiz_labels,
        "quiz_values": quiz_values,
        "revenue_month": revenue_month,
        "total_orders_month": total_orders_month,

        "order_status_labels_json": json.dumps(order_status_labels, ensure_ascii=False),
        "order_status_values_json": json.dumps(order_status_values),
        "payment_channels": payment_channels,

        # ✅ KPI Premium
        "premium_active": premium_active,
        "premium_activations_7d": premium_activations_7d,

        # ✅ Biểu đồ phân bổ gói (latest)
        "plan_labels_json": json.dumps(plan_labels, ensure_ascii=False),
        "plan_values_json": json.dumps(plan_values),

        # JSON cho các chart cũ
        "labels_7_json": json.dumps(labels_7, ensure_ascii=False),
        "signups_series_7_json": json.dumps(signups_series_7),
        "quiz_labels_json": json.dumps(quiz_labels, ensure_ascii=False),
        "quiz_values_json": json.dumps(quiz_values),
    }
    return render(request, "admin/dashboard.html", {**admin_ctx, **ctx})