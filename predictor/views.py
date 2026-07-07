from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixture, Prediction, Team
from .forms import PredictionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum


# Renders the public home page for the World Cup Hub.
# This is the landing page users see before choosing features such as
# fixtures, predictions, teams or Pontoon.
def home(request):
    return render(request, "predictor/home.html")


# Displays the fixture list page.
# Users can view all fixtures, filter by tournament stage, or filter
# group-stage fixtures by matchday.

# This is useful because the page also shows each user's own predictions.
@login_required
def fixture_list(request, stage=None, matchday=None):
    # Get the available tournament stages from the Fixture model.
    # These are used by the template to build the filter buttons/dropdown.
    stages = Fixture.STAGE_CHOICES

    # If a matchday is provided in the URL, only show group-stage fixtures
    # for that specific matchday.
    if matchday:
        fixtures = Fixture.objects.filter(
            stage="Group Stage",
            matchday=matchday
        )
        selected_stage = "Group Stage"
        selected_matchday = matchday

    # If a stage is provided in the URL, only show fixtures from that stage.
    # Example: Round of 16, Quarterfinals or Final.
    elif stage:
        fixtures = Fixture.objects.filter(stage=stage)
        selected_stage = stage
        selected_matchday = None

    # If no filter is selected, show every fixture.
    else:
        fixtures = Fixture.objects.all()
        selected_stage = "all"
        selected_matchday = None

    # Retrieve all predictions made by the logged-in user.
    # This lets the page show whether the user has already predicted a fixture.
    predictions = Prediction.objects.filter(user=request.user)

    # Store the user's predictions in a dictionary.
    # The fixture ID is used as the key, making it quick to look up
    # whether the user has predicted each fixture.
    prediction_map = {}

    for prediction in predictions:
        prediction_map[prediction.fixture.id] = prediction

    # Attach the user's prediction to each fixture object.
    # This creates a temporary attribute called user_prediction.
    # It is not stored in the database; it is only used by the template.
    for fixture in fixtures:
        fixture.user_prediction = prediction_map.get(fixture.id)

    # Data passed to the template.
    context = {
        "fixtures": fixtures,
        "stages": stages,
        "selected_stage": selected_stage,
        "selected_matchday": selected_matchday,
    }

    return render(request, "predictor/fixture_list.html", context)


# Allows a logged-in user to create or update a prediction for one fixture.
@login_required
def create_prediction(request, fixture_id):
    # Get the fixture being predicted.
    # If the fixture does not exist, Django returns a 404 error page.
    fixture = get_object_or_404(Fixture, id=fixture_id)

    # Stop users from creating or editing predictions once the fixture is locked.
    # This keeps the competition fair because users cannot change predictions after the match has started.
    if fixture.predictions_locked():
        messages.error(
            request,
            "Predictions are now locked for this fixture."
        )
        return redirect("fixtures")

    # Check whether this user has already made a prediction for this fixture.
    # If one exists, the form will update it instead of creating a duplicate.
    prediction = Prediction.objects.filter(
        user=request.user,
        fixture=fixture,
    ).first()

    # POST means the user has submitted the prediction form.
    if request.method == "POST":
        # Bind the submitted data to the form.
        # instance=prediction means the form updates an existing prediction
        # if one already exists, or creates a new one if prediction is None.
        form = PredictionForm(request.POST, instance=prediction)

        if form.is_valid():
            # commit=False creates the Prediction object but does not save it yet.
            # This gives us time to add the user and fixture, which are not
            # editable fields in the form.
            prediction = form.save(commit=False)
            prediction.fixture = fixture
            prediction.user = request.user

            # Save the prediction to the database.
            # The Prediction model also calculates points when saved.
            prediction.save()

            messages.success(
                request,
                "Prediction saved successfully!"
            )

            return redirect("fixtures")

    # GET means the user has opened the form page.
    # If a prediction already exists, the form is pre-filled with their scores.
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


# Saves predictions for multiple fixtures from the main fixture list page.
# This allows users to enter lots of predictions quickly without opening each fixture individually.
@login_required
def save_all_predictions(request):
    # Only process the form if the request method is POST.
    if request.method == "POST":
        # Get all fixtures because the submitted fixture list may contain
        # prediction fields for many different matches.
        fixtures = Fixture.objects.all()
        saved_count = 0

        for fixture in fixtures:
            # Each score input in the template uses the fixture ID in its name.
            # Example: home_12 and away_12 for fixture ID 12.
            home_score = request.POST.get(f"home_{fixture.id}")
            away_score = request.POST.get(f"away_{fixture.id}")

            # If either field is blank, ignore that fixture and move on.
            # This prevents empty score fields from creating invalid predictions.
            if home_score == "" or away_score == "":
                continue

            # If the fields do not exist in the submitted form, ignore the fixture.
            # This is a safety check in case only some fixtures were displayed.
            if home_score is None or away_score is None:
                continue

            # Do not save or update predictions for locked fixtures.
            # This prevents users from changing predictions after kick-off.
            if fixture.predictions_locked():
                continue

            # Create a new prediction or update the existing prediction
            # for this user and fixture.
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
# This gives users a personal dashboard where they can review their scores,
# see points awarded and edit/delete predictions where allowed.
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


# Allows a logged-in user to delete one of their own predictions.
@login_required
def delete_prediction(request, prediction_id):

    # Retrieve the prediction by ID, but also check it belongs to the current user.
    prediction = get_object_or_404(
        Prediction,
        id=prediction_id,
        user=request.user,
    )

    # Only delete the prediction after the user submits the confirmation form.
    # This prevents accidental deletion from simply visiting the page.
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


# Displays a leaderboard of users ranked by total prediction points.
@login_required
def leaderboard(request):

    # Group predictions by username, add up each user's points,
    # and order the results from highest score to lowest score.
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


# Shows all predictions for a specific fixture.
# This is intended to let users compare predictions once a fixture has locked.
@login_required
def fixture_predictions(request, fixture_id):
    fixture = get_object_or_404(Fixture, id=fixture_id)

    # IMPORTANT:
    # This view currently retrieves predictions even if the fixture is not locked.
    # If the template link is hidden before lock, normal users may not notice,
    # but someone could still visit the URL directly.
    #
    # If you want to fully enforce the rule, add a fixture.predictions_locked()
    # check here and redirect users if the fixture has not locked yet.
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


# Displays all World Cup teams in alphabetical order.
# This gives users a simple team directory/fact-file section.
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
# get_object_or_404 makes sure an invalid team ID shows a proper 404 page
# rather than breaking the application.
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