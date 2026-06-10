from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixture, Prediction
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum



def home(request):
    return render(request, "predictor/home.html")


@login_required
def fixture_list(request, stage=None):
    stages = Fixture.STAGE_CHOICES

    if stage:
        fixtures = Fixture.objects.filter(stage=stage)
        selected_stage = stage
    else:
        fixtures = Fixture.objects.all()
        selected_stage = "all"

    prediction_map = {}

    if request.user.is_authenticated:
        predictions = Prediction.objects.filter(user=request.user)

        for prediction in predictions:
            prediction_map[prediction.fixture.id] = prediction
    else:
        predictions = []

    context = {
        "fixtures": fixtures,
        "predictions": predictions,
        "stages": stages,
        "selected_stage": selected_stage,
        "prediction_map" :prediction_map,
    }

    return render(request, "predictor/fixture_list.html", context)

@login_required
def create_prediction(request, fixture_id):
    fixture = get_object_or_404(Fixture, id=fixture_id)

    if fixture.predictions_locked():
        messages.error(
            request,
            "Predictions are now locked for this fixture."
        )
        return redirect("fixtures")

    prediction = Prediction.objects.filter(
        user=request.user,
        fixture=fixture,
    ).first()

    if request.method == "POST":
        form = PredictionForm(request.POST, instance=prediction)
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
def save_all_predictions(request):
    if request.method == "POST":
        fixtures = Fixture.objects.all()

        saved_count = 0

        for fixture in fixtures:
            home_score = request.POST.get(f"home_{fixture.id}")
            away_score = request.POST.get(f"away_{fixture.id}")

            if home_score == "" or away_score == "":
                continue

            if fixture.predictions_locked():
                continue

            Prediction.objects.update_or_create(
                user=request.user,
                fixture=fixture,
                defaults={
                    "predicted_home_score": home_score,
                    "predicted_away_score": away_score,
                }
            )

            saved_count += 1

        messages.success(
            request,
            f"{saved_count} prediction(s) saved successfully."
        )

    return redirect(request.META.get("HTTP_REFERER", "fixtures"))


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

@login_required
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

@login_required
def fixture_predictions(request,fixture_id):
    fixture = get_object_or_404(Fixture, id=fixture_id)

    predictions = Prediction.objects.filter(
        fixture=fixture
    )

    context = {
        "fixture": fixture,
        "predictions": predictions,
    }

    return render(
        request,
        "predictor/fixture_predictions.html",
        context,
    )