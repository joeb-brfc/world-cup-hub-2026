from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixture, Prediction
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum



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

    prediction = Prediction.objects.filter(
        user=request.user,
        fixture=fixture,
    ).first()

    if request.method == "POST":
        form = PredictionForm(
            request.POST,
            instance=prediction,
        )

        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.fixture = fixture
            prediction.user = request.user
            prediction.save()

            messages.success(
                request,
                "Prediction saved successfully!"
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

@login_required
def my_predictions(request):
    predictions = Prediction.objects.filter(
        user=request.user
    )

    context = {
        "predictions": predictions,
    }

    return render(
        request,
        "predictor/my_predictions.html",
        context
    )

@login_required
def delete_prediction(request, prediction_id):

    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user,
    )

    if request.method == "POST":
        prediction.delete()

        messages.success(
            request,
            "Prediction deleted successfully!"
        )

        return redirect("my_predictions")

    context = {
        "prediction": prediction,
    }

    return render(
        request,
        "predictor/delete_prediction.html",
        context,
    )

def leaderboard(request):

    leaderboard = (
        Prediction.objects
        .values("user__username")
        .annotate(total_points=Sum("points_awarded"))
        .order_by("-total_points")
    )

    context = {
        "leaderboard": leaderboard,
    }

    return render(
        request,
        "predictor/leaderboard.html",
        context,
    )