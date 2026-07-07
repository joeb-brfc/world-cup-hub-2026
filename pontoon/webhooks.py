from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .webhook_handler import StripeWH_Handler
import stripe


# Receives webhook events sent from Stripe.
# Webhooks allow Stripe to notify the application when a payment
# succeeds, fails or another payment event occurs.
@csrf_exempt
def webhook(request):
    """
    Receives webhook events from Stripe.
    """

    # Retrieve the webhook payload and Stripe signature.
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    # Verify that the webhook request genuinely came from Stripe.
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WH_SECRET,
        )

    # Invalid payload.
    except ValueError:
        return HttpResponse(status=400)

    # Invalid Stripe signature.
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    print("Webhook verified")

    # Create an instance of the webhook handler.
    handler = StripeWH_Handler(request)

    # Map Stripe event types to their corresponding handler methods.
    event_map = {
        "payment_intent.succeeded":
            handler.handle_payment_intent_succeeded,

        "payment_intent.payment_failed":
            handler.handle_payment_intent_payment_failed,
    }

    # Process supported Stripe events.
    if event["type"] in event_map:
        return event_map[event["type"]](event)

    # Handle any other event types.
    return handler.handle_event(event)