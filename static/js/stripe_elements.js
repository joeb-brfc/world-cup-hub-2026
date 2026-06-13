const stripe = Stripe(stripePublicKey);
const elements = stripe.elements();

const card = elements.create("card");
card.mount("#card-element");

card.addEventListener("change", function(event) {
    const errorDiv = document.getElementById("card-errors");

    if (event.error) {
        errorDiv.textContent = event.error.message;
    } else {
        errorDiv.textContent = "";
    }
});

const form = document.getElementById("payment-form");
const submitButton = document.getElementById("submit-button");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    submitButton.disabled = true;
    submitButton.textContent = "Processing...";

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {
        if (result.error) {
            const errorDiv = document.getElementById("card-errors");
            errorDiv.textContent = result.error.message;

            submitButton.disabled = false;
            submitButton.textContent = "Pay to Play Pontoon";
        } else {
            if (result.paymentIntent.status === "succeeded") {
                window.location.href = successUrl + "?payment_intent=" + result.paymentIntent.id;
            }
        }
    });
});