from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# The Stadium model stores details about each World Cup stadium.
# Fixtures can link to a stadium so users can see where a match is being played.
class Stadium(models.Model):
    # Name of the stadium, for example "MetLife Stadium".
    name = models.CharField(max_length=100)

    # City where the stadium is located.
    city = models.CharField(max_length=100)

    # Stadium capacity is optional because this information may not always be needed.
    # blank=True allows the field to be left empty in forms/admin.
    # null=True allows the database to store an empty value.
    capacity = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        # This controls how the stadium appears in the Django admin and dropdowns.
        return self.name


# The Team model stores information about each nation taking part in the World Cup.
# It is used by fixtures, predictions and the Pontoon game.
class Team(models.Model):
    # These choices restrict the group field to valid World Cup groups only.
    # The first value is stored in the database, and the second value is shown to users/admin.
    GROUP_CHOICES = [
        ('A', 'Group A'),
        ('B', 'Group B'),
        ('C', 'Group C'),
        ('D', 'Group D'),
        ('E', 'Group E'),
        ('F', 'Group F'),
        ('G', 'Group G'),
        ('H', 'Group H'),
        ('I', 'Group I'),
        ('J', 'Group J'),
        ('K', 'Group K'),
        ('L', 'Group L'),
    ]

    # Team/nation name, for example "England" or "Brazil".
    name = models.CharField(max_length=100)

    # The World Cup group the team belongs to.
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)

    # Extra team information used to make the app more informative for users.
    # These fields are optional because some data may be missing or updated later.
    manager = models.CharField(max_length=100, blank=True, null=True)
    captain = models.CharField(max_length=100, blank=True, null=True)
    best_world_cup_finish = models.CharField(max_length=100, blank=True, null=True)
    best_world_cup_year = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        # This makes the team name display clearly in the admin, fixtures and dropdowns.
        return self.name


# The Fixture model stores each World Cup match.
# It links two teams together, stores kick-off time, stage, stadium and the final result.
class Fixture(models.Model):
    # These choices control which stage of the tournament a fixture belongs to.
    STAGE_CHOICES = [
        ('Group Stage', 'Group Stage'),
        ('Round of 32', 'Round of 32'),
        ('Round of 16', 'Round of 16'),
        ('Quarterfinals', 'Quarterfinals'),
        ('Semifinals', 'Semifinals'),
        ("Third Place", "Third Place Play-Off"),
        ("Final", "Final")
    ]

    # The home team for the fixture.
    # CASCADE so if a team is deleted, its related fixtures are also deleted.
    # related_name allows us to access all home fixtures from a Team object.
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_fixtures'
    )

    # The away team for the fixture.
    # A separate related_name is needed because Team is linked twice in this model.
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_fixtures'
    )

    # The stadium where the fixture is played.
    # SET_NULL so if a stadium is deleted, the fixture remains but the stadium becomes empty.
    stadium = models.ForeignKey(
        Stadium,
        on_delete=models.SET_NULL,
        related_name='fixtures',
        null=True,
        blank=True
    )

    # Tournament stage, such as Group Stage, Round of 16 or Final.
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)

    # Matchday is mainly used for group-stage filtering, for example matchday 1, 2 or 3.
    # It is optional because knockout matches do not need a group matchday.
    matchday = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    # Date and time when the match kicks off.
    # This is used to decide when predictions should lock.
    kickoff_time = models.DateTimeField()

    # Final match score.
    # These are optional because the result will not exist before the match is played.
    home_team_score = models.PositiveIntegerField(blank=True, null=True)
    away_team_score = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        # Fixtures are shown in kick-off order by default.
        ordering = ['kickoff_time']

    def __str__(self):
        # Useful readable name for the fixture in the admin and debug output.
        return f"{self.home_team} vs {self.away_team}"

    def predictions_locked(self):
        # Predictions are locked shortly after kick-off.
        # 1 minute is used to allow for any small time discrepancies between the server and user devices.
        # This prevents users from creating or editing predictions once the match has started.

        lock_time = self.kickoff_time + timedelta(minutes=1)
        return timezone.now() >= lock_time

    def update_prediction_points(self):
        # Get every prediction connected to this fixture.
        # This uses the related_name='predictions' from the Prediction model below.
        predictions = self.predictions.all()

        # Recalculate points for each prediction now that the fixture result may have changed.
        for prediction in predictions:
            prediction.points_awarded = prediction.calculate_points()

            # Update only the points_awarded field directly in the database.
            # This avoids calling prediction.save(), which helps prevent unnecessary repeated logic.
            Prediction.objects.filter(id=prediction.id).update(
                points_awarded=prediction.points_awarded
            )

    def save(self, *args, **kwargs):
        # First save the fixture normally.
        # This stores any new or updated fixture details/results in the database.
        super().save(*args, **kwargs)

        # After the fixture is saved, update all prediction scores linked to this match.
        self.update_prediction_points()

        # Import is placed inside the method to avoid circular import problems.
        # The predictor app needs to update Pontoon scores, but Pontoon also depends on teams/fixtures.
        from pontoon.models import update_all_pontoon_scores

        # Recalculate all Pontoon scores whenever a fixture result changes.
        update_all_pontoon_scores()


# The Prediction model stores one user's prediction for one specific fixture.
class Prediction(models.Model):
    # The user who made the prediction.
    # CASCADE so if a user is deleted, their predictions are also deleted.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    # The fixture being predicted.
    # CASCADE so if a fixture is deleted, its predictions are also deleted.
    fixture = models.ForeignKey(
        Fixture,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    # The score predicted by the user.
    predicted_home_score = models.PositiveIntegerField()
    predicted_away_score = models.PositiveIntegerField()

    # Points awarded for this prediction.
    # This is automatically calculated when the prediction is saved.
    points_awarded = models.IntegerField(default=0)

    # Timestamp showing when the prediction was first created.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can only make one prediction per fixture.
        # This prevents duplicate predictions for the same match.
        unique_together = ('user', 'fixture')

        # Predictions are shown in fixture kick-off order by default.
        ordering = ['fixture__kickoff_time']

    def __str__(self):
        # Readable display name for this prediction in the Django admin.
        return f"{self.user.username}'s prediction for {self.fixture}"

    def calculate_points(self):
        # Get the fixture linked to this prediction.
        fixture = self.fixture

        # No points can be awarded until both final scores have been entered.
        if (
            fixture.home_team_score is None or
            fixture.away_team_score is None
        ):
            return 0

        # Exact score prediction earns 3 points.
        # Example: predicted 2-1 and the actual result is 2-1.
        if (
            self.predicted_home_score == fixture.home_team_score and
            self.predicted_away_score == fixture.away_team_score
        ):
            return 3

        # If the score is not exact, calculate the match outcome.
        # A positive difference means home win.
        # A negative difference means away win.
        # Zero means draw.
        predicted_difference = (
            self.predicted_home_score - self.predicted_away_score
        )

        actual_difference = (
            fixture.home_team_score - fixture.away_team_score
        )

        # User predicted a home win, and the home team actually won.
        if predicted_difference > 0 and actual_difference > 0:
            return 1

        # User predicted an away win, and the away team actually won.
        if predicted_difference < 0 and actual_difference < 0:
            return 1

        # User predicted a draw, and the match actually ended as a draw.
        if predicted_difference == 0 and actual_difference == 0:
            return 1

        # Wrong score and wrong outcome earns 0 points.
        return 0

    def save(self, *args, **kwargs):
        # Recalculate points every time the prediction is saved.
        # This keeps the stored points_awarded value in sync with the fixture result.
        self.points_awarded = self.calculate_points()

        # Save the prediction normally after updating the points.
        super().save(*args, **kwargs)