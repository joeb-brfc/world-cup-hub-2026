from django.conf import settings
from django.http import HttpResponse
from .webhook_handler import StripeWH_Handler
import stripe


def webhook(request):
    """
    Receives webhook events from Stripe.
    """

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WH_SECRET,
        )

    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    print("Webhook verified")

    handler = StripeWH_Handler(request)

    event_map = {
        "payment_intent.succeeded":
            handler.handle_payment_intent_succeeded,

        "payment_intent.payment_failed":
            handler.handle_payment_intent_payment_failed,
    }

    if event["type"] in event_map:
        return event_map[event["type"]](event)

    return handler.handle_event(event)