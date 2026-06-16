// Initialise Stripe using the public key provided by Django.
const stripe = Stripe(stripePublicKey);

// Create Stripe Elements for secure card handling.
const elements = stripe.elements();

const card = elements.create("card");
card.mount("#card-element");


// Display validation errors while the user enters card details.
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


// Handle payment form submission.
form.addEventListener("submit", function(event) {
    event.preventDefault();

    // Prevent multiple submissions while payment is processing.
    submitButton.disabled = true;
    submitButton.textContent = "Processing...";

    // Confirm the payment using the Stripe PaymentIntent created by Django.
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
        }
    }).then(function(result) {

        // Display any Stripe payment errors to the user.
        if (result.error) {
            const errorDiv = document.getElementById("card-errors");

            errorDiv.textContent = result.error.message;

            submitButton.disabled = false;
            submitButton.textContent = "Pay to Play Pontoon";
        } else {

            // Redirect to the success page when payment completes successfully.
            if (result.paymentIntent.status === "succeeded") {
                window.location.href =
                    successUrl +
                    "?payment_intent=" +
                    result.paymentIntent.id;
            }
        }
    });
});