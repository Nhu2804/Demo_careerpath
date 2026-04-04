# home/views.py
from django.shortcuts import render
from django.http import JsonResponse
from quiz_highschool.models import ResultFeedback

PAGE_SIZE = 6  # Giữ lại nếu nơi khác còn dùng phân trang; trang chủ sẽ bỏ giới hạn

def home(request):
    qs = (ResultFeedback.objects
          .filter(approved=True, is_public=True, rating__gte=3)
          .select_related("user")
          .order_by("-rating", "-created_at"))
    # Bỏ giới hạn 6: lấy toàn bộ
    top_reviews = list(qs)
    has_more = False  # không còn "xem thêm"
    return render(request, "home.html", {
        "top_reviews": top_reviews,
        "has_more_reviews": has_more,
        "page_size": None,  # không còn dùng; có thể bỏ khỏi template
    })


def reviews_load(request):
    # Nếu bạn vẫn dùng endpoint này để load dần, có thể giữ phân trang
    offset = int(request.GET.get("offset", 0) or 0)
    qs = (ResultFeedback.objects
          .filter(approved=True, is_public=True, rating__gte=1)
          .select_related("user")
          .order_by("-rating", "-created_at"))

    items = [{
        "user": fb.user.username,  # dùng username
        "rating": fb.rating,
        "comment": fb.comment or "(Không có nội dung)",
        "created": fb.created_at.strftime("%d/%m/%Y %H:%M"),
    } for fb in qs[offset: offset + PAGE_SIZE]]

    next_offset = offset + PAGE_SIZE if qs.count() > offset + PAGE_SIZE else None
    return JsonResponse({"items": items, "next_offset": next_offset})
