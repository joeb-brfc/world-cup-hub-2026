from django.urls import path
from . import views

urlpatterns = [

    # Home page
    path("", views.home, name="home"),

    # Fixture and prediction routes
    path("fixtures/", views.fixture_list, name="fixtures"),

    path(
        "fixtures/save-all/",
        views.save_all_predictions,
        name="save_all_predictions",
    ),

    path(
        "fixtures/<int:fixture_id>/predict/",
        views.create_prediction,
        name="create_prediction",
    ),

    path(
        "fixtures/<int:fixture_id>/predictions/",
        views.fixture_predictions,
        name="fixture_predictions",
    ),

    # User prediction management
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

    # Leaderboard
    path(
        "leaderboard/",
        views.leaderboard,
        name="leaderboard",
    ),

    # Fixture filtering
    path(
        "fixtures/group-stage/matchday/<int:matchday>/",
        views.fixture_list,
        name="fixtures_by_matchday",
    ),

    path(
        "fixtures/<str:stage>/",
        views.fixture_list,
        name="fixtures_by_stage",
    ),

        # Team fact files
    path(
        "teams/",
        views.team_list,
        name="team_list",
    ),

    path(
        "teams/<int:team_id>/",
        views.team_detail,
        name="team_detail",
    ),
]