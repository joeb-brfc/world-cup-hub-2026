from django.shortcuts import render
from .models import PontoonBall


def pontoon_home(request):
    balls = PontoonBall.objects.all().order_by("number")

    context = {
        "balls": balls,
    }

    return render(request, "pontoon/pontoon_home.html", context)