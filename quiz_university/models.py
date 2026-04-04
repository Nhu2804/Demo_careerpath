from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation

class QuizUniversity(models.Model):
    """
    Lưu kết quả bài đánh giá kỹ năng sinh viên, gắn với từng user.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_university_attempts"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Nhóm ngành người dùng chọn ban đầu
    selected_cluster_code = models.CharField(max_length=50)
    selected_cluster_name = models.CharField(max_length=100)

    # Danh sách câu trả lời (list[list[int]])
    answers = models.JSONField(default=list)

    # Điểm kỹ năng theo từng nhóm kỹ năng
    # VD: {"technical_skills": 70, "soft_skills": 65, "creative_thinking": 80}
    skill_scores = models.JSONField(default=dict)

    # Đánh giá tổng quan mức độ sẵn sàng (0-100)
    readiness_score = models.PositiveIntegerField(default=0)

    # HTML phân tích chi tiết cho kết quả
    analysis_html = models.TextField()
    detailed_analysis_html = models.TextField(blank=True, null=True)

    # ResultFeedback (dùng chung model ở app THPT)
    feedbacks = GenericRelation("quiz_highschool.ResultFeedback", related_query_name="quiz_university")

    # Đề xuất hành động tiếp theo (optionally show in result page)
    recommended_actions = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.selected_cluster_name} ({self.readiness_score}%)"

    class Meta:
        verbose_name = "Bài đánh giá kỹ năng"
        verbose_name_plural = "Bài đánh giá kỹ năng"
        ordering = ["-created_at"]


# ===== Proxy: Phản hồi cho Đại học (trang admin riêng thuộc app này) =====
from quiz_highschool.models import ResultFeedback

class ResultFeedbackUniversity(ResultFeedback):
    class Meta:
        proxy = True
        app_label = "quiz_university"    # để hiển thị dưới menu Quiz_University
        verbose_name = "Feedback (SV)"
        verbose_name_plural = "Feedback (SV)"
