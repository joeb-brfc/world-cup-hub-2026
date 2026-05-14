from django.contrib import admin
from .models import Stadium, Team

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