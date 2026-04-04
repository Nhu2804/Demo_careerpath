# users/admin.py
from django.conf import settings
from datetime import timedelta, date  # 👈 thêm date
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User as DjangoUser
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django import forms
from django.shortcuts import redirect
from .models import CustomUser, SuperUserProxy, RegularUserProxy
from django.contrib.sessions.models import Session
from django.db.models import Q
from datetime import datetime

# Ẩn hẳn User mặc định để không trùng menu
try:
    admin.site.unregister(DjangoUser)
except admin.sites.NotRegistered:
    pass

# Nếu lỡ đăng ký CustomUser trước đó, hủy để chỉ dùng proxy
try:
    admin.site.unregister(CustomUser)
except admin.sites.NotRegistered:
    pass


# ========== QUẢN LÝ SUPERUSER: Nâng 1 user qua trang "Thêm" ==========
# users/admin.py
from django import forms
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.contrib import admin, messages

from .models import CustomUser, SuperUserProxy

# --- Form chọn user thường ---
# ---- Form chọn user để nâng ----
class PromoteForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.none(),
        label="Chọn người dùng để nâng thành Admin",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # chỉ lấy user chưa là superuser
        self.fields["user"].queryset = CustomUser.objects.filter(is_superuser=False)


@admin.register(SuperUserProxy)
class SuperUserProxyAdmin(admin.ModelAdmin):
    change_list_template = "control_manage_superusers.html"
    add_form_template    = "control_manage_superusers.html"

    list_display = (
        "username", "email", "active_status",
        "last_login_display", "date_joined_display",
        "promoted_by_name", "promoted_at_display",
    )
    search_fields = ("username", "email")
    list_filter = (
    "is_active",
    ("promoted_by", admin.RelatedOnlyFieldListFilter),
    ("promoted_at", admin.DateFieldListFilter),
)

    actions_on_top = True
   
    # Helper: format datetime an toàn cho cả naive/aware & USE_TZ on/off
    @staticmethod
    def _fmt_dt(dt):
        if not dt:
            return "-"
        try:
            # Nếu là naive và USE_TZ bật -> chuyển sang aware theo TZ hiện tại
            if timezone.is_naive(dt) and getattr(settings, "USE_TZ", False):
                dt = timezone.make_aware(dt, timezone.get_current_timezone())
            # Nếu đã aware -> đưa về localtime
            if timezone.is_aware(dt):
                dt = timezone.localtime(dt)
            return dt.strftime("%d/%m/%Y %H:%M")
        except Exception:
            # Dự phòng: format “thô” nếu có vấn đề
            return dt.strftime("%d/%m/%Y %H:%M")

    @admin.display(description="Lần cuối đăng nhập", ordering="last_login")
    def last_login_display(self, obj):
        return self._fmt_dt(obj.last_login)

    @admin.display(description="Ngày tham gia", ordering="date_joined")
    def date_joined_display(self, obj):
        return self._fmt_dt(obj.date_joined)

    @admin.display(description="Thời điểm nâng quyền", ordering="promoted_at")
    def promoted_at_display(self, obj):
        return self._fmt_dt(obj.promoted_at)

    @admin.display(description="Người nâng", ordering="promoted_by__username")
    def promoted_by_name(self, obj):
        return getattr(obj.promoted_by, "username", "—")
    
    @admin.display(description="Trạng thái")
    def active_status(self, obj):
        return format_html(
            '<span style="color:{}; font-weight:600;">{}</span>',
            "#28a745" if obj.is_active else "#dc3545",
            "Hoạt động" if obj.is_active else "Bị khóa"
    )

    # ====== ACTIONS: KHOÁ / MỞ KHOÁ ======
    @admin.action(description="🔒 Khoá đăng nhập")
    def lock_selected(self, request, queryset):
        # Không tự khoá chính mình
        if queryset.filter(pk=request.user.pk).exists():
            self.message_user(request, "❌ Không thể tự khoá tài khoản của chính bạn.", level=messages.ERROR)
            queryset = queryset.exclude(pk=request.user.pk)

        # Không khoá hết tất cả superuser đang hoạt động
        currently_active = CustomUser.objects.filter(is_superuser=True, is_active=True)
        will_lock_count = queryset.filter(is_active=True).count()
        if will_lock_count and currently_active.count() - will_lock_count <= 0:
            self.message_user(request, "❌ Không thể khoá toàn bộ Admin đang hoạt động (phải còn ít nhất 1).", level=messages.ERROR)
            return

        # Thực hiện khoá
        updated = queryset.update(is_active=False)
        # (Tuỳ chọn) đăng xuất cưỡng bức các phiên đang hoạt động
        self._force_logout(queryset)

        self.message_user(request, f"✅ Đã khoá {updated} tài khoản Admin.", level=messages.SUCCESS)

    @admin.action(description="🔓 Mở khoá")
    def unlock_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"✅ Đã mở khoá {updated} tài khoản Admin.", level=messages.SUCCESS)

    actions = ["demote_to_regular", "lock_selected", "unlock_selected"]  # 👈 thêm 2 action mới

    # ====== Helper: đăng xuất cưỡng bức người dùng (khi khoá) ======
    def _force_logout(self, users_queryset):
        """
        Xoá mọi session chứa các user này để đăng xuất ngay lập tức.
        Không bắt buộc, nhưng nên làm khi khoá.
        """
        user_ids = set(str(pk) for pk in users_queryset.values_list("pk", flat=True))
        for session in Session.objects.all():
            data = session.get_decoded()
            if data.get("_auth_user_id") in user_ids:
                session.delete()

    def get_queryset(self, request):
        qs = super().get_queryset(request).filter(is_superuser=True)
        return qs.select_related("promoted_by")

    # KHÔNG cho xoá trong màn này
    def has_delete_permission(self, request, obj=None):
        return False

    # Ẩn action xoá hàng loạt
    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    # -------- ACTION: hạ về user thường (KHÔNG xoá dữ liệu) --------
    @admin.action(description="⬇ Hạ xuống User")
    def demote_to_regular(self, request, queryset):
        updated = 0
        for u in queryset:
            if u.is_superuser or u.is_staff:
                u.is_superuser = False
                u.is_staff = False
                u.promoted_by = None
                u.promoted_at = None
                u.save(update_fields=["is_superuser", "is_staff"])
                updated += 1
        self.message_user(
            request,
            f"✅ Đã hạ {updated} tài khoản về người dùng thường.",
            level=messages.SUCCESS
        )



    # -------- Hiện form nâng ngay trang danh sách --------
    def changelist_view(self, request, extra_context=None):
        # Nếu là POST của Action admin (có 'action' trong POST), để Django xử lý
        if request.method == "POST" and request.POST.get("action"):
            return super().changelist_view(request, extra_context=extra_context)

        form = PromoteForm(request.POST or None)

        # Phân biệt POST của form nâng bằng cờ 'promote_user=1'
        if request.method == "POST" and request.POST.get("promote_user") == "1" and form.is_valid():
            u = form.cleaned_data["user"]
            u.is_superuser = True
            u.is_staff = True
            u.promoted_by = request.user          # ✅ Lưu người nâng
            u.promoted_at = timezone.now()
            u.save(update_fields=["is_superuser", "is_staff", "promoted_by", "promoted_at"])
            self.message_user(request, f"✅ Đã nâng “{u.username}” thành Admin.", level=messages.SUCCESS)
            return redirect("admin:users_superuserproxy_changelist")

        ctx = {"form": form, "title": "Quản lý Admin"}
        if extra_context:
            ctx.update(extra_context)
        return super().changelist_view(request, extra_context=ctx)

    # -------- Vẫn cho phép mở “Thêm” để nâng quyền --------
    def has_add_permission(self, request):
        return False

    def add_view(self, request, form_url="", extra_context=None):
        form = PromoteForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            u = form.cleaned_data["user"]
            u.is_superuser = True
            u.is_staff = True
            u.promoted_by = request.user          # ✅ Lưu người nâng
            u.promoted_at = timezone.now()
            u.save(update_fields=["is_superuser", "is_staff", "promoted_by", "promoted_at"])
            self.message_user(request, f"✅ Đã nâng “{u.username}” thành Admin.", level=messages.SUCCESS)
            return redirect("admin:users_superuserproxy_changelist")

        ctx = {"form": form, "title": "Nâng người dùng thành Admin"}
        if extra_context:
            ctx.update(extra_context)
        return TemplateResponse(request, self.add_form_template, ctx)



# ========== QUẢN LÝ USER THƯỜNG: Action nâng nhiều user cùng lúc ==========
@admin.register(RegularUserProxy)
class RegularUserAdmin(BaseUserAdmin):
    # ❌ BỎ dùng template tùy biến (nếu bạn không cần card nữa)
    # change_list_template = "control_manage_users.html"

    # Hiển thị
    list_display = (
        "avatar_preview", "username", "email", "is_active",
        "is_premium", "premium_expiry_display", "date_joined_display"
    )
    ordering        = ("-date_joined",)
    list_editable   = ("is_active", "is_premium")
    readonly_fields = ("date_joined", "last_login")

    # ✅ BẬT lại UI mặc định của Django
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter   = (
        "is_active",
        "is_premium",
        ("date_joined", admin.DateFieldListFilter),       # lọc theo ngày tham gia (mặc định)
        ("premium_expiry", admin.DateFieldListFilter),    # lọc theo ngày hết hạn
    )

    fieldsets = (
        ("Tài khoản", {"fields": ("username", "email", "password")}),
        ("Thông tin cá nhân", {"fields": ("first_name", "last_name", "avatar")}),
        ("Premium", {"fields": ("is_premium", "premium_expiry")}),
        ("Quyền", {"fields": ("is_active",)}),
        ("Lịch sử", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2",
                       "is_active", "is_premium", "premium_expiry"),
        }),
    )

    def get_queryset(self, request):
        # Chỉ loại superuser; KHÔNG đọc tham số GET tự chế nữa
        return super().get_queryset(request).filter(is_superuser=False)

    # --- Avatar xem trước ---
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="height:36px;border-radius:50%;" />', obj.avatar.url)
        return "—"
    avatar_preview.short_description = "Ảnh đại diện"

    # --- Định dạng ngày (dd/mm/YYYY HH:MM) ---
    @staticmethod
    def _fmt_dt(dt):
        if not dt:
            return "-"
        if timezone.is_naive(dt) and getattr(settings, "USE_TZ", False):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        if timezone.is_aware(dt):
            dt = timezone.localtime(dt)
        return dt.strftime("%d/%m/%Y %H:%M")

    @admin.display(description="Ngày tham gia", ordering="date_joined")
    def date_joined_display(self, obj):
        return self._fmt_dt(obj.date_joined)

    @admin.display(description="Hết hạn Premium", ordering="premium_expiry")
    def premium_expiry_display(self, obj):
        return self._fmt_dt(obj.premium_expiry)

    # --- Actions của bạn giữ nguyên (nếu cần) ---
    @admin.action(description="🔼 Nâng thành Admin")
    def promote_to_superuser(self, request, queryset):
        qs = queryset.filter(is_superuser=False)
        updated = 0
        for u in qs:
            u.is_superuser = True
            u.is_staff = True
            if hasattr(u, "promoted_by"):
                u.promoted_by = request.user
            if hasattr(u, "promoted_at"):
                u.promoted_at = timezone.now()
            u.save(update_fields=["is_superuser", "is_staff",
                                  *(["promoted_by"] if hasattr(u,"promoted_by") else []),
                                  *(["promoted_at"] if hasattr(u,"promoted_at") else [])])
            updated += 1
        self.message_user(request, f"✅ Đã nâng {updated} người dùng thành Admin.", level=messages.SUCCESS)

    @admin.action(description="📧 Gửi email cảnh báo Premium sắp hết hạn")
    def notify_premium_expiry(self, request, queryset):
        sent = 0
        for u in queryset:
            if u.is_premium and u.premium_expiry and u.premium_expiry <= timezone.now() + timedelta(days=7):
                send_mail(
                    subject="⚠ Premium sắp hết hạn",
                    message="Tài khoản Premium của bạn sẽ hết hạn trong 7 ngày. Vui lòng gia hạn để tiếp tục sử dụng.",
                    from_email="admin@yourapp.com",
                    recipient_list=[u.email],
                )
                sent += 1
        self.message_user(request, f"📨 Đã gửi email cho {sent} tài khoản Premium.", level=messages.SUCCESS)

    actions = ["promote_to_superuser", "notify_premium_expiry"]


    def save_model(self, request, obj, form, change):
        # Nếu admin tick Premium mà chưa đặt hạn, tự gán 30 ngày
        if obj.is_premium and not obj.premium_expiry:
            obj.premium_expiry = timezone.now() + timedelta(days=30)
        super().save_model(request, obj, form, change)

