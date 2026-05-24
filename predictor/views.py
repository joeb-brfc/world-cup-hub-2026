from django.shortcuts import render
from .models import Fixture



def home(request):
    return render(request, "predictor/home.html")

def fixture_list(request):

    group_fixtures = Fixture.objects.filter(stage="group")

    last_32_fixtures = Fixture.objects.filter(stage="last_32")

    last_16_fixtures = Fixture.objects.filter(stage="last_16")

    quarter_final_fixtures = Fixture.objects.filter(stage="quarter_final")

    semi_final_fixtures = Fixture.objects.filter(stage="semi_final")

    final_fixtures = Fixture.objects.filter(stage="final")

    context = {
        "group_fixtures": group_fixtures,
        "last_32_fixtures": last_32_fixtures,
        "last_16_fixtures": last_16_fixtures,
        "quarter_final_fixtures": quarter_final_fixtures,
        "semi_final_fixtures": semi_final_fixtures,
        "final_fixtures": final_fixtures,
    }

    return render(request, "predictor/fixture_list.html", context)