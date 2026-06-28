from django.http import HttpResponse


def webhook(request):
    """
    Receives webhook events from Stripe.
    """

    print("Webhook received")

    return HttpResponse(status=200)