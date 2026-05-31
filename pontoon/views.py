from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import PontoonBall


def pontoon_home(request):
    balls = PontoonBall.objects.all().order_by("number")

    context = {
        "balls": balls,
    }

    return render(request, "pontoon/pontoon_home.html", context)

@login_required
def select_ball(request, ball_id):

    ball = get_object_or_404(
        PontoonBall,
        id=ball_id
    )

    return redirect("pontoon_home")