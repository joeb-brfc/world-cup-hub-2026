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
        Handles successful payment events from Stripe.
        """

        intent = event.data.object

        print("PaymentIntent succeeded:")
        print(intent.id)
        print(intent.metadata)

        return HttpResponse(
            content="Webhook received: payment_intent.succeeded",
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