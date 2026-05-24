from django.shortcuts import render
from .models import Fixture



def home(request):
    return render(request, "predictor/home.html")

def fixtures_list(request):
    fixtures = Fixturee.objects.all()

    context = {
        "fixtures": fixtures
    }
    return render(request, "predictor/fixtures_list.html", context)