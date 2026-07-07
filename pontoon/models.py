# Models for the premium World Cup Pontoon game.
# Users select a numbered football, receive a random team,
# and score points throughout the tournament based on that team's results.

from django.db import models
from django.contrib.auth.models import User
from predictor.models import Team
from predictor.models import Fixture


# Stores each numbered football used in the Pontoon game.
# Every football can be assigned one World Cup team and selected by one user.
class PontoonBall(models.Model):

    # The football number displayed to users.
    number = models.PositiveIntegerField(unique=True)

    # Randomly assigned World Cup team.
    # SET_NULL allows the football to remain even if a team is removed.
    team = models.OneToOneField(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # The user who selected this football.
    # One user can only own one football.
    selected_by = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Current Pontoon score.
    score = models.IntegerField(
        default=0
    )

    # Indicates whether the team has gone above 21 points.
    busted = models.BooleanField(
        default=False
    )

    # Calculates the Pontoon score using all completed fixtures.
    def calculate_score(self):

        # A football without a team cannot score points.
        if not self.team:
            return 0

        score = 0

        # Retrieve every fixture involving the assigned team.
        fixtures = Fixture.objects.filter(
            models.Q(home_team=self.team)
            |
            models.Q(away_team=self.team)
        )

        for fixture in fixtures:

            # Ignore fixtures that do not yet have a result.
            if (
                fixture.home_team_score is None
                or
                fixture.away_team_score is None
            ):
                continue

            # Calculate the score via 2 points for each goal scored and -1 point for each goal conceded.

            if fixture.home_team == self.team:

                # Goals scored = +2 points.
                score += (
                    fixture.home_team_score * 2
                )

                # Goals conceded = -1 point.
                score -= (
                    fixture.away_team_score
                )

            else:

                score += (
                    fixture.away_team_score * 2
                )

                score -= (
                    fixture.home_team_score
                )

        return score

    # Updates the team's current Pontoon score.
    def update_score(self):

        # Once a team is bust, its score remains fixed.
        if self.busted:
            return

        self.score = self.calculate_score()

        # A score above 21 means the team has gone bust.
        if self.score > 21:
            self.busted = True

        self.save()

    def __str__(self):
        # Display the football number in the Django admin.
        return f"Football {self.number}"


# Recalculate the scores for every football in the game.
# This is called whenever a fixture result is updated.
def update_all_pontoon_scores():
    for ball in PontoonBall.objects.all():
        ball.update_score()


# Stores payment and access details for the premium Pontoon game.
class PontoonAccess(models.Model):

    # User linked to the Pontoon subscription.
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="pontoon_access"
    )

    # Determines whether the user has access to the premium game.
    has_access = models.BooleanField(default=False)

    # Stripe payment identifier used for payment tracking.
    stripe_pid = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # Amount paid for entry.
    amount_paid = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    # Date and time the access record was created.
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        # Display the username in the Django admin.
        return f"{self.user.username} Pontoon Access"