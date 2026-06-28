from decimal import Decimal

from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import PontoonAccess


class StripeWH_Handler:
    """
    Handles Stripe webhook events.
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handles generic or unexpected webhook events.
        """

        return HttpResponse(
            content=f"Unhandled webhook received: {event['type']}",
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Grants Pontoon access when Stripe confirms a successful payment.
        """

        intent = event.data.object

        payment_intent_id = intent.id
        user_id = intent.metadata.get("user_id")
        product = intent.metadata.get("product")

        if product != "World Cup Pontoon Access":
            return HttpResponse(
                content="Webhook ignored: not Pontoon access.",
                status=200
            )

        if not user_id:
            return HttpResponse(
                content="Webhook ignored: missing user_id metadata.",
                status=200
            )

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            return HttpResponse(
                content="Webhook ignored: user not found.",
                status=200
            )

        access, created = PontoonAccess.objects.get_or_create(
            user=user
        )

        access.has_access = True
        access.stripe_pid = payment_intent_id

        amount = getattr(intent, "amount_received", None) or intent.amount
        access.amount_paid = Decimal(amount) / Decimal("100")

        access.save()

        return HttpResponse(
            content="Pontoon access granted from Stripe webhook.",
            status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handles failed payment events.
        """

        return HttpResponse(
            content="Webhook received: payment_intent.payment_failed",
            status=200
        )