# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# import openai
# import traceback

# # Config Together.ai as OpenAI-compatible
# client = openai.OpenAI(
#     api_key="tgp_v1_CBrB9SCvE4jnW-Gp3R1QcUN6NII80DVNQX0GQPPtz34",  # Thay bằng API key từ Together.ai
#     base_url="https://api.together.xyz"
# )

# # Trang giới thiệu và bắt đầu bài test
# def gioi_thieu(request):
#     return render(request, 'gioi_thieu.html')

# def question_hs(request):
#     return render(request, 'question_hs.html')

# def build_prompt(answers):
#     joined = "; ".join(answers)
#     first_choice = answers[0].lower()

#     if "tin học" in first_choice or "công nghệ" in first_choice:
#         domain = "lập trình, phát triển phần mềm, công nghệ"
#     elif "toán" in first_choice or "vật lý" in first_choice:
#         domain = "khoa học, logic, toán học"
#     elif "ngữ văn" in first_choice or "lịch sử" in first_choice:
#         domain = "ngôn ngữ, xã hội, truyền thông"
#     elif "mỹ thuật" in first_choice or "thiết kế" in first_choice:
#         domain = "nghệ thuật, thiết kế, sáng tạo"
#     elif "sinh học" in first_choice or "giáo dục công dân" in first_choice:
#         domain = "tâm lý, sinh học, giáo dục"
#     else:
#         domain = "các nhóm ngành phổ biến"

#     return (
#         f"Dựa trên các câu trả lời trước đó ({joined}), hãy viết **một câu hỏi trắc nghiệm giúp đánh giá học sinh hợp với ngành nghề nào** "
#         f"trong lĩnh vực {domain}. Câu hỏi không được lặp lại từ khóa đã có trong câu trả lời trước và phải thể hiện một trong các khía cạnh: "
#         f"năng lực, hành vi, xu hướng phản ứng, kỹ năng làm việc nhóm, hoặc thói quen học tập. KHÔNG chỉ hỏi 'thích' hoặc 'muốn'.\n\n"
#         f"⚠️ Trả về đúng định dạng sau (không thêm mô tả hay lời dẫn):\n"
#         f"Câu hỏi X:\n"
#         f"<Câu hỏi rõ ràng, không trùng với lựa chọn>\n"
#         f"A. <Lựa chọn 1>\n"
#         f"B. <Lựa chọn 2>\n"
#         f"C. <Lựa chọn 3>\n"
#         f"D. <Lựa chọn 4>\n"
#         f"(E. <Lựa chọn 5> nếu cần)\n"
#         f"⚠️ Không được nhắc lại trực tiếp từ câu hỏi trong các đáp án."

#     )


# @csrf_exempt
# def next_question(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         answers = data.get("answers", [])

#         # Câu hỏi 1 cố định
#         if len(answers) == 0:
#             return JsonResponse({
#                 "question": "Bạn yêu thích môn học nào nhất?",
#                 "options": [
#                     '<i class="fas fa-book-open"></i> Ngữ văn, Lịch sử, Địa lý',
#                     '<i class="fas fa-laptop-code"></i> Tin học, Công nghệ',
#                     '<i class="fas fa-flask"></i> Toán học, Vật lý, Hóa học',
#                     '<i class="fas fa-palette"></i> Mỹ thuật, Âm nhạc, Thiết kế',
#                     '<i class="fas fa-seedling"></i> Sinh học, Giáo Dục Công Dân, Tâm lý học'
#                 ]
#             })

#         # Các câu sau dùng model
#         prompt = build_prompt(answers)
#         try:
#             response = client.completions.create(
#                 model="mistralai/Mixtral-8x7B-Instruct-v0.1",
#                 prompt=prompt,
#                 max_tokens=512,
#                 temperature=0.7,
#                 top_p=0.9
#             )

#             lines = [line.strip() for line in response.choices[0].text.split('\n') if line.strip()]
#             question = ""
#             options = []

#             # Tìm dòng chứa "Câu hỏi"
#             for i, line in enumerate(lines):
#                 if line.lower().startswith("câu hỏi"):
#                     if i + 1 < len(lines):
#                         question = lines[i + 1]
#                         options = lines[i + 2:i + 7]  # Lấy A-D hoặc A-E nếu có
#                     break

#             if not question or len(options) < 4:
#                 return JsonResponse({"error": "Không thể tạo câu hỏi hợp lệ"}, status=500)

#             # Format lại các lựa chọn cho frontend (giữ nguyên A/B/C)
#             options_cleaned = []
#             icons = [
#                 '<i class="fas fa-book-open"></i> ',
#                 '<i class="fas fa-laptop-code"></i> ',
#                 '<i class="fas fa-flask"></i> ',
#                 '<i class="fas fa-palette"></i> ',
#                 '<i class="fas fa-seedling"></i> ',
#             ]
#             for idx, opt in enumerate(options[:5]):
#                 parts = opt.split(".", 1)
#                 if len(parts) == 2:
#                     options_cleaned.append(f"{icons[idx]}{parts[1].strip()}")
#                 else:
#                     options_cleaned.append(f"{icons[idx]}{opt.strip()}")

#             return JsonResponse({
#                 "question": question,
#                 "options": options_cleaned[:5]
#             })


#         except Exception as e:
#             traceback.print_exc()
#             return JsonResponse({"error": f"Lỗi hệ thống: {str(e)}"}, status=500)