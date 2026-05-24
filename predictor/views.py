from django.shortcuts import render, get_object_or_404, redirect
from .models import Fixture, Prediction
from .forms import PredictionForm



def home(request):
    return render(request, "predictor/home.html")

def fixture_list(request):
    fixtures = Fixture.objects.all()

    context = {
        "fixtures": fixtures
    }
    return render(request, "predictor/fixture_list.html", context)

def create_prediction(request, fixture_id):
    fixture = get_object_or_404(Fixture, id=fixture_id)

    if request.method == "POST":
        form = PredictionForm(request.POST)

        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.fixture = fixture
            prediction.user = request.user
            prediction.save()
            return redirect("fixtures")
    else:
        form = PredictionForm()

    context = {
        "form": form,
        "fixture": fixture,
    }

    return render(request, "predictor/create_prediction.html", context)