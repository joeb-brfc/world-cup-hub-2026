import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PontoonBall, PontoonAccess


# Displays the Pontoon game.
# Only users who have purchased access can enter the game.
@login_required
def pontoon_home(request):

    # Check whether the logged-in user has paid for Pontoon access.
    access = PontoonAccess.objects.filter(
        user=request.user,
        has_access=True
    ).exists()

    # Redirect users without access to the checkout page.
    if not access:
        return redirect("pontoon_checkout")

    # Display all footballs in numerical order.
    balls = PontoonBall.objects.all().order_by("number")

    # Build the Pontoon leaderboard using footballs that have been selected.
    # Active teams are shown first, followed by busted teams.
    leaderboard_balls = PontoonBall.objects.filter(
        selected_by__isnull=False
    ).order_by("busted", "-score")

    # Retrieve the football selected by the current user, if one exists.
    selected_ball = PontoonBall.objects.filter(
        selected_by=request.user
    ).first()

    # Retrieve the current winning Pontoon team, if one has reached exactly 21.
    winner_ball = PontoonBall.objects.filter(
        selected_by__isnull=False,
        score=21,
        busted=False
    ).first()

    context = {
        "balls": balls,
        "leaderboard_balls": leaderboard_balls,
        "selected_ball": selected_ball,
        "winner_ball": winner_ball,
    }

    return render(request, "pontoon/pontoon_home.html", context)

# Allows a user to select one numbered football.
@login_required
def select_ball(request, ball_id):

    # Retrieve the selected football.
    ball = get_object_or_404(
        PontoonBall,
        id=ball_id
    )

    # Prevent users selecting a football that has already been claimed.
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

    # Assign the football to the logged-in user.
    ball.selected_by = request.user
    ball.save()

    messages.success(
        request,
        "You have selected a football."
    )

    return redirect("pontoon_home")


# Displays the countdown and confirmation page before revealing a football.
@login_required
def confirm_ball(request, ball_id):

    ball = get_object_or_404(
        PontoonBall,
        id=ball_id
    )

    # Prevent users accessing the confirmation page for an already selected football.
    if ball.selected_by:
        messages.error(
            request,
            "That football has already been taken."
        )
        return redirect("pontoon_home")

    already_selected = PontoonBall.objects.filter(
        selected_by=request.user
    ).exists()

    # Prevent users who already own a football from accessing this page.
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


# Creates a Stripe PaymentIntent for premium Pontoon access.
@login_required
def pontoon_checkout(request):

    # Use the Stripe secret key stored in the project's settings.
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Create a PaymentIntent ready for Stripe Checkout.
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


# Displays the payment success page after a successful Stripe payment.
# User access is granted by the Stripe webhook, not by this view.
@login_required
def pontoon_payment_success(request):

    payment_intent = request.GET.get("payment_intent")

    context = {
        "payment_intent": payment_intent,
    }

    return render(
        request,
        "pontoon/pontoon_payment_success.html",
        context,
    )