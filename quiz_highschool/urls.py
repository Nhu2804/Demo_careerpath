from django.urls import path
from . import views

app_name = 'quiz_highschool'

urlpatterns = [
    path('gioi-thieu/', views.gioi_thieu, name='gioi_thieu'),
    path('trac-nghiem/', views.question_hs, name='question_hs'),
    path('api/next-question/', views.next_question, name='next_question'),
    path('ket-qua/', views.ket_qua, name='ket_qua'),
    path('submit/', views.calculate_result, name='submit'),
    path("feedback/", views.save_feedback, name="save_feedback"),

]


