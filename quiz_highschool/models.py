from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator


class QuizHighschool(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_highschool_attempts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Lưu câu trả lời (20 câu, mỗi câu có thể chọn nhiều đáp án)
    answers = models.JSONField(default=list)

    # Lưu kết quả phần trăm mỗi nhóm ngành
    cluster_percentages = models.JSONField(default=dict)

    # Nhóm ngành phù hợp nhất
    top_cluster_code = models.CharField(max_length=20)
    top_cluster_name = models.CharField(max_length=100)
    top_percentage = models.FloatField()

    # Nhóm ngành phù hợp thứ 2
    second_cluster_code = models.CharField(max_length=20)
    second_cluster_name = models.CharField(max_length=100)
    second_percentage = models.FloatField()

    # Lưu sẵn bài phân tích HTML để hiển thị nhanh
    top_analysis_html = models.TextField()
    second_analysis_html = models.TextField(blank=True, null=True)

    feedbacks = GenericRelation("quiz_highschool.ResultFeedback", related_query_name="quiz_highschool")

    def __str__(self):
        return f"{self.user.username} - {self.top_cluster_name} ({self.top_percentage}%)"

    class Meta:
        verbose_name = "Bài test HS"
        verbose_name_plural = "Bài test HS"


class ResultFeedback(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_feedbacks",
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)
    object_id = models.PositiveIntegerField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)

    # Việt hoá nhãn để hiện đẹp trong admin
    approved = models.BooleanField("Đã duyệt", default=False, db_index=True)
    is_public = models.BooleanField("Công khai", default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Phản hồi kết quả"
        verbose_name_plural = "Phản hồi kết quả"
        indexes = [
            models.Index(fields=["content_type", "object_id"], name="idx_ct_obj"),
            models.Index(fields=["approved", "is_public", "rating", "created_at"], name="idx_moderation_stats"),
            models.Index(fields=["user", "content_type", "object_id"], name="idx_owner_ct_obj"),
        ]

    def __str__(self):
        return f"{self.rating}★ by {self.user} on {self.content_type.model}#{self.object_id}"

    @property
    def masked_user(self):
        full = (getattr(self.user, "get_full_name", None) or (lambda: ""))() or self.user.username
        parts = full.strip().split()
        return f"{parts[0]} {parts[-1][0]}." if len(parts) > 1 else parts[0]


# Proxy: Phản hồi cho THPT (admin riêng, không tạo bảng mới)
class ResultFeedbackHighschool(ResultFeedback):
    class Meta:
        proxy = True
        verbose_name = "Feedback (HS)"
        verbose_name_plural = "Feedback (HS)"
