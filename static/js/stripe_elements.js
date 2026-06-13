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