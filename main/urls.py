# home/urls.py
from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.home, name="home"),
    path("reviews/load/", views.reviews_load, name="reviews_load"),  # ⬅️ API load-more
]
