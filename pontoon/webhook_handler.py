from django.http import HttpResponse

from .models import PontoonAccess


# Handles incoming Stripe webhook events.
class StripeWH_Handler:

    def __init__(self, request):
        # Store the incoming webhook request.
        self.request = request

    # Handles webhook events that do not have a dedicated handler.
    def handle_event(self, event):

        return HttpResponse(
            content=f"Unhandled webhook received: {event['type']}",
            status=200
        )

    # Handles successful Stripe payments.
    def handle_payment_intent_succeeded(self, event):

        intent = event.data.object

        print("PaymentIntent succeeded:")
        print(intent.id)
        print(intent.metadata)

        return HttpResponse(
            content="Webhook received: payment_intent.succeeded",
            status=200
        )

    # Handles failed Stripe payment attempts.
    def handle_payment_intent_payment_failed(self, event):

        return HttpResponse(
            content="Webhook received: payment_intent.payment_failed",
            status=200
        )