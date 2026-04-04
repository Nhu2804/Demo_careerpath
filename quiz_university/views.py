from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json
from collections import defaultdict

from .models import QuizUniversity
from .question_bank import QUESTION_BANKS
from django.views.decorators.http import require_POST
#from .analysis_generator import generate_analysis_html
from django.views.decorators.http import require_http_methods
from .generate_analysis_html import generate_analysis_html_social, generate_analysis_html_business, generate_analysis_html_tech, generate_analysis_html_health, generate_analysis_html_arts, generate_analysis_html_science, generate_detailed_analysis_html
from premium.models import PremiumSubscription


def gioi_thieu(request):
    return render(request, 'gioi_thieu_u.html')

@login_required
@require_http_methods(["GET", "POST"])
def select_cluster(request):
    if request.method == "POST":
        code = request.POST.get("selected_cluster_code")
        name = request.POST.get("selected_cluster_name")
        if not (code and name):
            return render(request, "select_cluster_u.html", {"error": "Thiếu thông tin nhóm ngành."})

        # clear state cũ nếu có
        request.session.pop("quiz_university_result_id", None)
        request.session.pop("quiz_answers", None)

        request.session["selected_cluster_code"] = code
        request.session["selected_cluster_name"] = name
        return redirect("quiz_university:question_u")

    return render(request, "select_cluster_u.html")



@login_required
@require_http_methods(["GET", "POST"])
def question_u(request):
    code = request.session.get("selected_cluster_code")
    name = request.session.get("selected_cluster_name")
    if not (code and name):
        return redirect("quiz_university:select_cluster_u")

    # Lưu tạm câu trả lời vào session nếu bạn submit từng câu bằng form POST
    if request.method == "POST":
        answers = request.session.get("quiz_answers", {})
        qid = request.POST.get("question_id")
        ans = request.POST.get("answer")
        if qid and ans:
            answers[qid] = ans
            request.session["quiz_answers"] = answers
        if request.POST.get("submit") == "1":  # bấm nút Nộp bài
            return redirect("quiz_university:submit_quiz_u")

    return render(request, "question_u.html", {
        "selected_cluster_code": code,
        "selected_cluster_name": name,
    })


@require_POST
@login_required
def next_question_u(request):
    data = json.loads(request.body)
    question_index = data.get("question_index", 0)

    cluster_code = request.session.get('selected_cluster_code')
    QUESTION_BANK = QUESTION_BANKS.get(cluster_code, [])

    if question_index < len(QUESTION_BANK):
        q = QUESTION_BANK[question_index]

        return JsonResponse({
            "question": q["question"],
            "options": q["options"]
        })
    else:
        return JsonResponse({"end": True})

@require_POST
@login_required
def submit_quiz_u(request):
    data = json.loads(request.body)
    answers = data.get("answers", [])

    cluster_code = request.session.get('selected_cluster_code')
    QUESTION_BANK = QUESTION_BANKS.get(cluster_code, [])

    if not isinstance(answers, list):
        return JsonResponse({"status": "error", "message": "Dữ liệu câu trả lời không hợp lệ."}, status=400)

    answers = answers[:len(QUESTION_BANK)]
    while len(answers) < len(QUESTION_BANK):
        answers.append([])

    category_scores = defaultdict(list)
    total_score = 0
    total_count = 0

    for idx, selected_list in enumerate(answers):
        if idx >= len(QUESTION_BANK):
            break
        q = QUESTION_BANK[idx]
        if not selected_list:
            continue
        avg_score = sum(selected_list) / len(selected_list)
        category_scores[q["category"]].append(avg_score)
        total_score += avg_score
        total_count += 1

    skill_scores = {
        category: round(sum(scores) / len(scores) * 100 / 4, 2)
        for category, scores in category_scores.items() if scores
    }
    readiness_score = round(total_score / total_count * 100 / 4, 2) if total_count else 0

    # ✅ Sửa ở đây:
    analysis_html = generate_analysis_html(cluster_code, skill_scores, readiness_score)
    detailed_analysis_html = generate_detailed_analysis_html(cluster_code, skill_scores, readiness_score)

    try:
        # ✅ Tạo bản ghi mới khi nộp bài
        quiz_result = QuizUniversity.objects.create(
            user=request.user,
            selected_cluster_code=cluster_code,
            selected_cluster_name=request.session.get('selected_cluster_name', ''),
            answers=answers,
            skill_scores=skill_scores,
            readiness_score=readiness_score,
            analysis_html=analysis_html,
            detailed_analysis_html=detailed_analysis_html,
            updated_at=timezone.now()
        )

        # ✅ Lưu ID vào session để dùng cho trang kết quả
        request.session['quiz_university_result_id'] = quiz_result.id

    except Exception as e:
        return JsonResponse({"status": "error", "message": "Không thể lưu kết quả."}, status=500)

    return JsonResponse({"status": "ok", "redirect": "/quiz_university/ket-qua/"})


# Đặt ở đầu views.py hoặc utils.py
def format_score(score):
    if score == int(score):
        return str(int(score))
    else:
        return f"{score:.1f}"

@login_required
def ket_qua_u(request):
    quiz_result_id = request.GET.get('quiz_id') or request.session.get('quiz_university_result_id')

    # ✅ Tính premium giống highschool
    subscription = PremiumSubscription.objects.filter(user=request.user).first()
    is_premium = subscription.check_status() if subscription else False

    context = {}

    if quiz_result_id:
        try:
            quiz_result = QuizUniversity.objects.get(id=quiz_result_id, user=request.user)
            cluster_code = quiz_result.selected_cluster_code
            skill_scores = quiz_result.skill_scores
            readiness_score = quiz_result.readiness_score

            analysis_html = generate_analysis_html(cluster_code, skill_scores, readiness_score)
            detailed_analysis_html = generate_detailed_analysis_html(cluster_code, skill_scores, readiness_score)

            order = ["Kỹ năng mềm", "Kỹ năng chuyên môn", "Tư duy sáng tạo"]
            skill_scores_display = {k: format_score(v) for k, v in skill_scores.items()}
            skill_scores_sorted = {k: skill_scores_display[k] for k in order if k in skill_scores_display}

            context = {
                "selected_cluster_name": quiz_result.selected_cluster_name,
                "readiness_score": format_score(readiness_score),
                "skill_scores": skill_scores_sorted,
                "analysis_html": analysis_html,
                "detailed_analysis_html": detailed_analysis_html,

                "quiz_type": "university",
                "quiz_id": quiz_result.id,

                # ⬇️ TRUYỀN TRẠNG THÁI PREMIUM XUỐNG TEMPLATE
                "is_premium": is_premium,
            }
        except QuizUniversity.DoesNotExist:
            context = {
                "error": "Kết quả không tồn tại.",
                "is_premium": is_premium,  # vẫn truyền xuống để template xử lý
            }
    else:
        context = {
            "error": "Bạn chưa làm bài đánh giá.",
            "is_premium": is_premium,  # vẫn truyền xuống để template xử lý
        }

    return render(request, 'result_u.html', context)


def generate_analysis_html(cluster_code, skill_scores, readiness_score):
    cluster_mapping = {
        "social": generate_analysis_html_social,
        "business": generate_analysis_html_business,
        "tech": generate_analysis_html_tech,
        "health": generate_analysis_html_health,
        "arts": generate_analysis_html_arts,
        "science": generate_analysis_html_science,
    }
    try:
        func = cluster_mapping[cluster_code]
    except KeyError:
        raise ValueError(f"Invalid cluster_code: {cluster_code}")
    return func(skill_scores, readiness_score)




