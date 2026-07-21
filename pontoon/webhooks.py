import logging

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .webhook_handler import StripeWH_Handler


logger = logging.getLogger(__name__)


@csrf_exempt
def webhook(request):
    """
    Receives, verifies and processes Stripe webhook events.
    """

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    if not sig_header:
        logger.error("Stripe signature header was missing.")

        return HttpResponse(
            content="Missing Stripe signature.",
            status=400,
        )

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WH_SECRET,
        )

    except ValueError:
        logger.exception("Invalid Stripe webhook payload.")

        return HttpResponse(
            content="Invalid payload.",
            status=400,
        )

    except stripe.error.SignatureVerificationError:
        logger.exception("Stripe webhook signature verification failed.")

        return HttpResponse(
            content="Invalid signature.",
            status=400,
        )

    event_type = event["type"]

    logger.info(
        "Verified Stripe webhook: %s",
        event_type,
    )

    handler = StripeWH_Handler(request)

    event_map = {
        "payment_intent.succeeded":
            handler.handle_payment_intent_succeeded,

        "payment_intent.payment_failed":
            handler.handle_payment_intent_payment_failed,
    }

    event_handler = event_map.get(
        event_type,
        handler.handle_event,
    )

    try:
        return event_handler(event)

    except Exception:
        logger.exception(
            "Unexpected error processing Stripe event %s.",
            event_type,
        )

        return HttpResponse(
            content="Webhook processing failed.",
            status=500,
        )