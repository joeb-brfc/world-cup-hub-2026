from django.urls import path
from . import views

urlpatterns = [
    path("", views.pontoon_home, name="pontoon_home"),
]