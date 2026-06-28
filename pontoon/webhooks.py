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

    return handler.handle_event(event)