import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PontoonBall, PontoonAccess


@login_required
def pontoon_home(request):
    # Used for the football grid, so balls stay in number order.
    balls = PontoonBall.objects.all().order_by("number")

    # Used for the leaderboard, so highest active scores appear first.
    leaderboard_balls = PontoonBall.objects.filter(
        selected_by__isnull=False
    ).order_by("busted", "-score")

    selected_ball = PontoonBall.objects.filter(
        selected_by=request.user
    ).first()

    context = {
        "balls": balls,
        "leaderboard_balls": leaderboard_balls,
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

def confirm_ball(request, ball_id):
    ball = get_object_or_404(PontoonBall, id=ball_id)

    return render(
        request,
        "pontoon/confirm_ball.html",
        {
            "ball": ball,
        }
    )

@login_required
def pontoon_checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    intent = stripe.PaymentIntent.create(
        amount=settings.STRIPE_PONTOON_PRICE,
        currency="gbp",
        metadata={
            "user_id": request.user.id,
            "username": request.user.username,
            "product": "World Cup Pontoon Access",
        },
    )

    context = {
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": intent.client_secret,
    }

    return render(request, "pontoon/pontoon_checkout.html", context)