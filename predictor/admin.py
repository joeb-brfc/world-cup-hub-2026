from django.contrib import admin
from .models import Fixture, Prediction, Stadium, Team


# Admin configuration for stadium records
@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity')
    search_fields = ('name', 'city')


# Admin configuration for participating teams
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'manager', 'captain')
    list_filter = ('group',)
    search_fields = ('name', 'manager', 'captain')


# Admin configuration for World Cup fixtures
@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = (
        "home_team",
        "away_team",
        "stadium",
        "stage",
        "matchday",
        "kickoff_time",
        "home_team_score",
        "away_team_score",
    )

    list_filter = (
        "stage",
        "matchday",
        "kickoff_time",
    )

    search_fields = (
        "home_team__name",
        "away_team__name",
    )


# Admin configuration for user predictions
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'fixture',
        'predicted_home_score',
        'predicted_away_score',
        'points_awarded'
    )

    list_filter = (
        'fixture',
        'user'
    )

    search_fields = (
        'user__username',
    )