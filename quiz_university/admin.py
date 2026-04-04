from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter, BooleanFieldListFilter
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType

from .models import QuizUniversity, ResultFeedbackUniversity
from quiz_highschool.models import ResultFeedback


from django.utils import timezone
from django.conf import settings

# ===== Utils =====
def _fmt_pct(value):
    try:
        return f"{float(value):.0f}%"
    except (TypeError, ValueError):
        return ""

# ===== Bộ lọc tiếng Việt =====
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

class SelectedClusterNameVN(admin.SimpleListFilter):
    title = "ngành đã chọn"
    parameter_name = "selected_cluster_name"
    def lookups(self, request, model_admin):
        values = (model_admin.model.objects.order_by()
                  .values_list("selected_cluster_name", flat=True).distinct())
        return [(v, v) for v in values if v]
    def queryset(self, request, qs):
        return qs.filter(selected_cluster_name=self.value()) if self.value() else qs

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

# ===== Admin: Bài đánh giá kỹ năng (ĐH) =====
@admin.register(QuizUniversity)
class QuizUniversityAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)

    @admin.display(description="Người dùng")
    def nguoi_dung(self, obj): return obj.user

    @admin.display(description="Ngành đã chọn")
    def cum_nganh_da_chon(self, obj): return obj.selected_cluster_name

    @admin.display(description="Mức sẵn sàng")
    def muc_san_sang(self, obj): return _fmt_pct(obj.readiness_score)

    @admin.display(description="Số câu trả lời")
    def so_cau_tra_loi(self, obj):
        try: return len(obj.answers or [])
        except TypeError: return 0

    @admin.display(description="Thời gian tạo", ordering="created_at")
    def thoi_gian_tao(self, obj):
        if not obj.created_at:
            return "-"
        dt = obj.created_at
        if timezone.is_naive(dt) and getattr(settings, "USE_TZ", False):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        if timezone.is_aware(dt):
            dt = timezone.localtime(dt)
        return dt.strftime("%d/%m/%Y %H:%M")  # ✅ dùng /


    list_display = ("nguoi_dung", "cum_nganh_da_chon", "muc_san_sang", "so_cau_tra_loi", "thoi_gian_tao")
    list_display_links = ("nguoi_dung", "cum_nganh_da_chon")
    list_filter = (("created_at", CreatedAtVN), SelectedClusterNameVN)
    search_fields = ("user__username", "user__email", "selected_cluster_name", "selected_cluster_code")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    inlines = [ResultFeedbackInline]

    fieldsets = (
        ("Thông tin chung", {"fields": ("user", "created_at", "updated_at")}),
        ("Lựa chọn ban đầu", {"fields": ("selected_cluster_code", "selected_cluster_name")}),
        ("Câu trả lời & điểm kỹ năng", {"fields": ("answers", "skill_scores", "readiness_score")}),
        ("Phân tích kết quả", {"fields": ("analysis_html", "detailed_analysis_html", "recommended_actions")}),
    )

# ===== Admin: Phản hồi kết quả (ĐH) – proxy, có cột Nhận xét & edit inline công khai/duyệt =====
@admin.register(ResultFeedbackUniversity)
class ResultFeedbackDHAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)

    @admin.display(description="Người gửi")
    def nguoi_gui(self, obj):
        return obj.user

    @admin.display(description="Nhận xét")
    def nhan_xet(self, obj):
        return obj.comment or ""

    @admin.display(description="Đối tượng được phản hồi")
    def doi_tuong(self, obj):
        target = obj.content_object
        if isinstance(target, QuizUniversity):
            return f"Bài đánh giá ĐH #{target.pk} – {target.selected_cluster_name or '—'}"
        return f"{obj.content_type.model}#{obj.object_id}"

    @admin.display(description="Thời gian tạo", ordering="created_at")
    def thoi_gian_tao(self, obj):
        if not obj.created_at:
            return "-"
        dt = obj.created_at
        if timezone.is_naive(dt) and getattr(settings, "USE_TZ", False):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        if timezone.is_aware(dt):
            dt = timezone.localtime(dt)
        return dt.strftime("%d/%m/%Y %H:%M")  # ✅ dùng /

    list_display = (
        "nguoi_gui",
        "rating",
        "nhan_xet",
        "is_public",  # chỉ giữ công khai
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

    # Chỉ hiện phản hồi của QuizUniversity
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        ct = ContentType.objects.get_for_model(QuizUniversity)
        return qs.filter(content_type=ct)

    def has_add_permission(self, request):
        return False
