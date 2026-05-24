from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("fixtures/", views.fixture_list, name="fixtures"),
    path(
        "fixtures/<int:fixture_id>/predict/",
        views.create_prediction,
        name="create_prediction",
    ),
]