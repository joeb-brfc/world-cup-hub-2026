from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PontoonBall


def pontoon_home(request):
    balls = PontoonBall.objects.all().order_by("number")

    selected_ball = None

    if request.user.is_authenticated:
        selected_ball = PontoonBall.objects.filter(
            selected_by=request.user
        ).first()

    context = {
        "balls": balls,
        "selected_ball": selected_ball,
    }

    return render(request, "pontoon/pontoon_home.html", context)

@login_required
def select_ball(request, ball_id):

    ball = get_object_or_404(
        PontoonBall,
        id=ball_id
    )

    if ball.selected_by:
        messages.error(
            request,
            "That football has already been taken."
        )
        return redirect("pontoon_home")
    
    already_selected = PontoonBall.objects.filter(
        selected_by=request.user
    ).exists()

    if already_selected:
        messages.error(
            request,
            "You have already selected a football."
        )
        return redirect("pontoon_home")

    ball.selected_by = request.user
    ball.save()
    messages.success(
        request,
        "You have selected a football."
    )
    return redirect("pontoon_home")