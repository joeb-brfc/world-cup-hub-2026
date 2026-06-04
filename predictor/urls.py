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
    path(
        "my-predictions/",
        views.my_predictions,
        name="my_predictions",
    ),

    path(
    "prediction/<int:prediction_id>/delete/",
    views.delete_prediction,
    name="delete_prediction",
    ),

    path(
    "leaderboard/",
    views.leaderboard,
    name="leaderboard",
    ),
    
    path(
    "fixtures/<str:stage>/",
    views.fixture_list,
    name="fixtures_by_stage",
    ),

    path(
    "fixtures/<int:fixture_id>/predictions/",
    views.fixture_predictions,
    name="fixture_predictions",
    ),

]