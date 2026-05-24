from django.shortcuts import render
from .models import Fixture



def home(request):
    return render(request, "predictor/home.html")

def fixture_list(request):
    fixtures = Fixture.objects.all()

    context = {
        "fixtures": fixtures
    }
    return render(request, "predictor/fixture_list.html", context)