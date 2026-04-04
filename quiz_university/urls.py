from django.urls import path
from . import views

app_name = 'quiz_university'

urlpatterns = [
    path('gioi-thieu/', views.gioi_thieu, name='gioi_thieu_u'),
    path('trac-nghiem/', views.question_u, name='question_u'),
    path('api/next-question/', views.next_question_u, name='next_question_u'),
    path('chon-nhom-nganh/', views.select_cluster, name='select_cluster_u'),
    path('submit/', views.submit_quiz_u, name='submit_quiz_u'),
    path('ket-qua/', views.ket_qua_u, name='ket_qua_u'),
]
    