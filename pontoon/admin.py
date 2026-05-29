from django.contrib import admin
from .models import PontoonBall


@admin.register(PontoonBall)
class PontoonBallAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "team",
        "selected_by",
    )

    list_filter = (
        "team",
        "selected_by",
    )

    search_fields = (
        "number",
        "team__name",
        "selected_by__username",
    )