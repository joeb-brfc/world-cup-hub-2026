from django import forms
from .models import Prediction


# This form allows users to create or edit a prediction for a fixture.
# using the fields defined in the Prediction model.
class PredictionForm(forms.ModelForm):

    class Meta:
        # Tell Django which model this form is linked to.
        # When the form is submitted, Django knows how to create
        # or update a Prediction object in the database.
        model = Prediction

        # Only include the score prediction fields.
        # The remaining fields (user, fixture, points_awarded and created_at)
        # are populated automatically by the application and should not be
        # editable by users.
        fields = [
            "predicted_home_score",
            "predicted_away_score",
        ]