from django.contrib import admin
from .models import Fixture, Prediction, Stadium, Team

@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'capacity')
    search_fields = ('name', 'city')

# Register your models here.

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'manager', 'captain')
    list_filter = ('group',)
    search_fields = ('name', 'manager', 'captain')

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
    list_display = ('home_team', 'away_team', 'stadium', 'stage', 'kickoff_time', 'home_team_score', 'away_team_score')
    list_filter = ('stage', 'kickoff_time')
    search_fields = ('home_team__name', 'away_team__name')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'fixture', 'predicted_home_score', 'predicted_away_score', 'points_awarded')
    list_filter = ('fixture','user')
    search_fields = ('user__username',)
