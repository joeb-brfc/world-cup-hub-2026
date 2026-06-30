from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixture, Prediction, Team
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum


# Renders the home page.
def home(request):
    return render(request, "predictor/home.html")


# Displays fixtures, with optional filtering by stage or group matchday.
@login_required
def fixture_list(request, stage=None, matchday=None):
    stages = Fixture.STAGE_CHOICES

    # Filter group stage fixtures by matchday.
    if matchday:
        fixtures = Fixture.objects.filter(
            stage="Group Stage",
            matchday=matchday
        )
        selected_stage = "Group Stage"
        selected_matchday = matchday

    # Filter fixtures by knockout stage.
    elif stage:
        fixtures = Fixture.objects.filter(stage=stage)
        selected_stage = stage
        selected_matchday = None

    # Display all fixtures when no filter is selected.
    else:
        fixtures = Fixture.objects.all()
        selected_stage = "all"
        selected_matchday = None

    # Retrieve the logged-in user's predictions.
    predictions = Prediction.objects.filter(user=request.user)

    # Store predictions in a dictionary for quick fixture lookup.
    prediction_map = {}

    for prediction in predictions:
        prediction_map[prediction.fixture.id] = prediction

    # Attach the user's existing prediction to each fixture for template display.
    for fixture in fixtures:
        fixture.user_prediction = prediction_map.get(fixture.id)

    context = {
        "fixtures": fixtures,
        "stages": stages,
        "selected_stage": selected_stage,
        "selected_matchday": selected_matchday,
    }

    return render(request, "predictor/fixture_list.html", context)


# Allows a user to create or update a prediction for one fixture.
@login_required
def create_prediction(request, fixture_id):
    fixture = get_object_or_404(Fixture, id=fixture_id)

    # Prevent predictions from being changed after the fixture is locked.
    if fixture.predictions_locked():
        messages.error(
            request,
            "Predictions are now locked for this fixture."
        )
        return redirect("fixtures")

    # Check whether the user has already predicted this fixture.
    prediction = Prediction.objects.filter(
        user=request.user,
        fixture=fixture,
    ).first()

    # Save the submitted form if the request is POST.
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

    # Load a blank or pre-filled form for GET requests.
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


# Saves predictions for multiple fixtures from the fixture list page.
@login_required
def save_all_predictions(request):
    if request.method == "POST":
        fixtures = Fixture.objects.all()
        saved_count = 0

        for fixture in fixtures:
            home_score = request.POST.get(f"home_{fixture.id}")
            away_score = request.POST.get(f"away_{fixture.id}")

            # Ignore fixtures where either score field has been left blank.
            if home_score == "" or away_score == "":
                continue

            # Ignore fixtures that were not included in the submitted form.
            if home_score is None or away_score is None:
                continue

            # Prevent updates to predictions once the fixture has locked.
            if fixture.predictions_locked():
                continue

            # Create a new prediction or update the user's existing one.
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

    return redirect("fixtures")


# Displays all predictions made by the logged-in user.
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


# Allows a user to delete one of their own predictions.
@login_required
def delete_prediction(request, prediction_id):

    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user,
    )

    # Only delete the prediction after the confirmation form is submitted.
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


# Displays users ranked by their total prediction points.
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


# Shows all predictions for a fixture once predictions are locked.
@login_required
def fixture_predictions(request, fixture_id):
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

# Displays all World Cup teams.
def team_list(request):
    teams = Team.objects.all().order_by("name")

    context = {
        "teams": teams,
    }

    return render(
        request,
        "predictor/team_list.html",
        context,
    )


# Displays one World Cup team fact file.
def team_detail(request, team_id):
    team = get_object_or_404(
        Team,
        id=team_id,
    )

    context = {
        "team": team,
    }

    return render(
        request,
        "predictor/team_detail.html",
        context,
    )