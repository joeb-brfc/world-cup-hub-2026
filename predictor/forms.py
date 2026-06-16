from django import forms
from .models import Prediction


# Form used to create and update match predictions
class PredictionForm(forms.ModelForm):

    class Meta:
        model = Prediction

        fields = [
            "predicted_home_score",
            "predicted_away_score",
        ]