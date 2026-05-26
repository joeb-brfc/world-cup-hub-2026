from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixture, Prediction
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def home(request):
    return render(request, "predictor/home.html")

def fixture_list(request):
    fixtures = Fixture.objects.all()

    if request.user.is_authenticated:
        predictions = Prediction.objects.filter(user=request.user)
    else:
        predictions = []

    context = {
        "fixtures": fixtures,
        "predictions": predictions,
    }

    return render(request, "predictor/fixture_list.html", context)

@login_required
def create_prediction(request, fixture_id):

    fixture = get_object_or_404(Fixture, id=fixture_id)

    prediction, created = Prediction.objects.get_or_create(
        user=request.user,
        fixture=fixture,
    )

    if request.method == "POST":

        form = PredictionForm(request.POST, instance=prediction)

        if form.is_valid():

            form.save()

            if created:
                messages.success(
                    request,
                    "Prediction created successfully!"
                )

            else:
                messages.success(
                    request,
                    "Prediction updated successfully!"
                )

            return redirect("fixtures")

    else:
        form = PredictionForm(instance=prediction)

    context = {
        "form": form,
        "fixture": fixture,
    }

    return render(
        request,
        "predictor/create_prediction.html",
        context
    )