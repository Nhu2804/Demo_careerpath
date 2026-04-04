from django.contrib import admin
from django.utils.html import format_html_join
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin.filters import DateFieldListFilter, BooleanFieldListFilter
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings

from .models import (
    QuizHighschool,
    ResultFeedback,
    ResultFeedbackHighschool,
)


def _fmt_dt(dt):
    if not dt:
        return "-"
    # Nếu datetime naive và USE_TZ bật → make_aware
    if timezone.is_naive(dt) and getattr(settings, "USE_TZ", False):
        dt = timezone.make_aware(dt, timezone.get_current_timezone())
    if timezone.is_aware(dt):
        dt = timezone.localtime(dt)
    return dt.strftime("%d/%m/%Y %H:%M")  # ✅ dạng dd/mm/YYYY


# ===== Utils =====
def _fmt_pct(value):
    try:
        return f"{float(value):.0f}%"
    except (TypeError, ValueError):
        return ""

# ===== Filter tiếng Việt =====
class CreatedAtVN(DateFieldListFilter):
    title = "Thời gian tạo"

class ApprovedVN(BooleanFieldListFilter):
    title = "Trạng thái duyệt"

class IsPublicVN(BooleanFieldListFilter):
    title = "Công khai"

class RatingVN(admin.SimpleListFilter):
    title = "Điểm đánh giá"
    parameter_name = "rating"
    def lookups(self, request, model_admin):
        return [(str(i), f"{i}★") for i in range(1, 6)]
    def queryset(self, request, qs):
        return qs.filter(rating=self.value()) if self.value() else qs

class TopClusterNameVN(admin.SimpleListFilter):
    title = "Ngành (phù hợp nhất)"
    parameter_name = "top_cluster_name"
    def lookups(self, request, model_admin):
        values = (model_admin.model.objects.order_by()
                  .values_list("top_cluster_name", flat=True).distinct())
        return [(v, v) for v in values if v]
    def queryset(self, request, qs):
        return qs.filter(top_cluster_name=self.value()) if self.value() else qs

class SecondClusterNameVN(admin.SimpleListFilter):
    title = "Ngành (phù hợp thứ hai)"
    parameter_name = "second_cluster_name"
    def lookups(self, request, model_admin):
        values = (model_admin.model.objects.order_by()
                  .values_list("second_cluster_name", flat=True).distinct())
        return [(v, v) for v in values if v]
    def queryset(self, request, qs):
        return qs.filter(second_cluster_name=self.value()) if self.value() else qs

# ===== Inline phản hồi =====
class ResultFeedbackInline(GenericTabularInline):
    model = ResultFeedback
    extra = 0
    ct_field = "content_type"
    ct_fk_field = "object_id"
    fields = ("user", "rating", "comment", "approved", "is_public", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
    verbose_name = "Phản hồi"
    verbose_name_plural = "Danh sách phản hồi"

# ===== Admin: Bài làm THPT =====
@admin.register(QuizHighschool)
class QuizHighschoolAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)

    @admin.display(description="Người dùng")
    def nguoi_dung(self, obj): return obj.user

    @admin.display(description="Ngành phù hợp nhất")
    def nganh_phu_hop_nhat(self, obj): return obj.top_cluster_name

    @admin.display(description="Tỉ lệ phù hợp nhất")
    def ti_le_phu_hop_nhat(self, obj): return _fmt_pct(obj.top_percentage)

    @admin.display(description="Ngành phù hợp thứ hai")
    def nganh_phu_hop_thu_hai(self, obj): return obj.second_cluster_name

    @admin.display(description="Tỉ lệ phù hợp thứ hai")
    def ti_le_phu_hop_thu_hai(self, obj): return _fmt_pct(obj.second_percentage)

    @admin.display(description="Số câu trả lời")
    def so_cau_tra_loi(self, obj):
        try: return len(obj.answers or [])
        except TypeError: return 0

    @admin.display(description="Tóm tắt tỉ lệ các ngành")
    def tom_tat_cac_nganh(self, obj):
        data = obj.cluster_percentages or {}
        if not isinstance(data, dict): return ""
        items = []
        for code, pct in data.items():
            try: items.append((code, float(pct)))
            except (TypeError, ValueError): pass
        top3 = sorted(items, key=lambda kv: kv[1], reverse=True)[:3]
        return format_html_join(", ", "{}: {}", ((code, _fmt_pct(pct)) for code, pct in top3))

    @admin.display(description="Thời gian tạo", ordering="created_at")
    def thoi_gian_tao(self, obj):
        return _fmt_dt(obj.created_at)

    list_display = (
        "nguoi_dung", "nganh_phu_hop_nhat", "ti_le_phu_hop_nhat",
        "nganh_phu_hop_thu_hai", "ti_le_phu_hop_thu_hai",
        "so_cau_tra_loi", "tom_tat_cac_nganh", "thoi_gian_tao",
    )
    list_display_links = ("nguoi_dung", "nganh_phu_hop_nhat")
    list_filter = (("created_at", CreatedAtVN), TopClusterNameVN, SecondClusterNameVN)
    search_fields = (
        "user__username", "user__email",
        "top_cluster_name", "second_cluster_name",
        "top_cluster_code", "second_cluster_code",
    )
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    inlines = [ResultFeedbackInline]

    fieldsets = (
        ("Thông tin người làm bài", {"fields": ("user", "created_at", "updated_at")}),
        ("Chi tiết câu trả lời & tỉ lệ", {"fields": ("answers", "cluster_percentages")}),
        ("ngành phù hợp nhất", {"fields": ("top_cluster_code", "top_cluster_name", "top_percentage", "top_analysis_html")}),
        ("ngành phù hợp thứ hai", {"fields": ("second_cluster_code", "second_cluster_name", "second_percentage", "second_analysis_html")}),
    )

# ===== Admin: Phản hồi kết quả (THPT) – proxy, có cột Nhận xét & edit inline công khai/duyệt =====
@admin.register(ResultFeedbackHighschool)
class ResultFeedbackTHPTAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)

    @admin.display(description="Người gửi")
    def nguoi_gui(self, obj):
        return obj.user  # hiện thẳng user

    @admin.display(description="Nhận xét")
    def nhan_xet(self, obj):
        return obj.comment or ""

    @admin.display(description="Đối tượng được phản hồi")
    def doi_tuong(self, obj):
        target = obj.content_object
        if isinstance(target, QuizHighschool):
            return f"Bài làm THPT #{target.pk} – {target.top_cluster_name or '—'}"
        return f"{obj.content_type.model}#{obj.object_id}"

    @admin.display(description="Thời gian tạo", ordering="created_at")
    def thoi_gian_tao(self, obj):
        return _fmt_dt(obj.created_at)

    list_display = (
        "nguoi_gui",
        "rating",
        "nhan_xet",
        "is_public",   # chỉ giữ công khai
        "doi_tuong",
        "thoi_gian_tao",
    )
    list_display_links = ("nguoi_gui", "doi_tuong")
    list_editable = ("is_public",)

    list_filter = (("is_public", IsPublicVN), RatingVN, ("created_at", CreatedAtVN))
    search_fields = ("user__username", "user__email", "comment")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    actions = ["cho_cong_khai", "an_phan_hoi"]

    @admin.action(description="Cho công khai phản hồi")
    def cho_cong_khai(self, request, queryset):
        updated = queryset.update(is_public=True)
        self.message_user(request, f"Đã cho công khai {updated} phản hồi.")

    @admin.action(description="Ẩn phản hồi")
    def an_phan_hoi(self, request, queryset):
        updated = queryset.update(is_public=False)
        self.message_user(request, f"Đã ẩn {updated} phản hồi.")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        ct = ContentType.objects.get_for_model(QuizHighschool)
        return qs.filter(content_type=ct)

    def has_add_permission(self, request):
        return False
