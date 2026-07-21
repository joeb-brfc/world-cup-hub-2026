import logging
from decimal import Decimal

from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import PontoonAccess


logger = logging.getLogger(__name__)


class StripeWH_Handler:
    """
    Handles Stripe webhook events for Pontoon payments.
    """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handles Stripe events without a dedicated handler.
        """

        event_type = event["type"]

        logger.info(
            "Unhandled Stripe webhook received: %s",
            event_type,
        )

        return HttpResponse(
            content=f"Unhandled webhook received: {event_type}",
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """
        Grants Pontoon access after Stripe confirms payment.
        """

        intent = event["data"]["object"]

        payment_intent_id = intent["id"]
        metadata = intent["metadata"]

        user_id = (
            metadata["user_id"]
            if "user_id" in metadata
            else None
        )

        product = (
            metadata["product"]
            if "product" in metadata
            else None
        )

        amount_received = (
            intent["amount_received"]
            if "amount_received" in intent
            else 0
        )

        logger.info(
            "Processing successful PaymentIntent %s for user %s.",
            payment_intent_id,
            user_id,
        )

        # A real Pontoon payment must include the user's database ID.
        if not user_id:
            logger.error(
                "PaymentIntent %s has no user_id metadata.",
                payment_intent_id,
            )

            return HttpResponse(
                content="Missing user_id metadata.",
                status=400,
            )

        # Ignore successful payments for unrelated products.
        if product != "World Cup Pontoon Access":
            logger.warning(
                "PaymentIntent %s ignored because product metadata was %s.",
                payment_intent_id,
                product,
            )

            return HttpResponse(
                content="Payment does not relate to Pontoon access.",
                status=200,
            )

        try:
            user = User.objects.get(
                pk=int(user_id)
            )

        except (User.DoesNotExist, TypeError, ValueError):
            logger.exception(
                "Unable to find user %s for PaymentIntent %s.",
                user_id,
                payment_intent_id,
            )

            return HttpResponse(
                content="User not found.",
                status=400,
            )

        try:
            access, created = PontoonAccess.objects.get_or_create(
                user=user,
            )

            access.has_access = True
            access.stripe_pid = payment_intent_id

            # Stripe sends payment amounts in the smallest currency unit.
            # For GBP, 500 represents £5.00.
            access.amount_paid = (
                Decimal(str(amount_received))
                / Decimal("100")
            )

            access.save()

        except Exception:
            logger.exception(
                "Failed to grant Pontoon access for PaymentIntent %s.",
                payment_intent_id,
            )

            # Return a genuine error so Stripe knows processing failed.
            return HttpResponse(
                content="Unable to grant Pontoon access.",
                status=500,
            )

        logger.info(
            "Pontoon access granted to user %s. Record created: %s.",
            user.username,
            created,
        )

        return HttpResponse(
            content="Pontoon access granted.",
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """
        Acknowledges a failed Stripe payment.
        """

        intent = event["data"]["object"]
        payment_intent_id = intent["id"]

        logger.warning(
            "PaymentIntent failed: %s",
            payment_intent_id,
        )

        return HttpResponse(
            content="Payment failure acknowledged.",
            status=200,
        )