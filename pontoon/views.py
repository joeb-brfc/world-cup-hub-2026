import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PontoonBall, PontoonAccess


# Displays the Pontoon game page for users with access.
@login_required
def pontoon_home(request):
    access = PontoonAccess.objects.filter(
        user=request.user,
        has_access=True
    ).exists()

    if not access:
        return redirect("pontoon_checkout")

    balls = PontoonBall.objects.all().order_by("number")

    # Leaderboard only includes footballs that have been selected.
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


# Assigns a football to the logged-in user.
@login_required
def select_ball(request, ball_id):
    ball = get_object_or_404(
        PontoonBall,
        id=ball_id
    )

    # Prevent users selecting a football that has already been taken.
    if ball.selected_by:
        messages.error(
            request,
            "That football has already been taken."
        )
        return redirect("pontoon_home")

    already_selected = PontoonBall.objects.filter(
        selected_by=request.user
    ).exists()

    # Prevent users selecting more than one football.
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


# Shows a confirmation page before the football is selected.
@login_required
def confirm_ball(request, ball_id):
    ball = get_object_or_404(
        PontoonBall,
        id=ball_id
    )

    # Prevent the confirmation page showing for a football already taken.
    if ball.selected_by:
        messages.error(
            request,
            "That football has already been taken."
        )
        return redirect("pontoon_home")

    already_selected = PontoonBall.objects.filter(
        selected_by=request.user
    ).exists()

    # Prevent users who already have a football reaching the confirmation page.
    if already_selected:
        messages.error(
            request,
            "You have already selected a football."
        )
        return redirect("pontoon_home")

    return render(
        request,
        "pontoon/confirm_ball.html",
        {
            "ball": ball,
        }
    )


# Creates a Stripe PaymentIntent for Pontoon access.
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


# Grants Pontoon access after a successful payment redirect.
@login_required
def pontoon_payment_success(request):
    payment_intent = request.GET.get("payment_intent")

    access, created = PontoonAccess.objects.get_or_create(
        user=request.user
    )

    access.has_access = True
    access.stripe_pid = payment_intent
    access.save()

    context = {
        "payment_intent": payment_intent,
    }

    return render(
        request,
        "pontoon/pontoon_payment_success.html",
        context
    )