from django.urls import path
from . import views

urlpatterns = [
    path("", views.pontoon_home, name="pontoon_home"),
    path(
    "select/<int:ball_id>/",
    views.select_ball,
    name="select_ball",
),
    path(
    "confirm/<int:ball_id>/",
    views.confirm_ball,
    name="confirm_ball",
),
    
]