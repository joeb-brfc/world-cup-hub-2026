from django.db import models
from django.contrib.auth.models import User
from predictor.models import Team
from predictor.models import Fixture


# Stores the numbered footballs used in the Pontoon game.
class PontoonBall(models.Model):

    number = models.PositiveIntegerField(unique=True)

    team = models.OneToOneField(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    selected_by = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    score = models.IntegerField(
        default=0
    )

    busted = models.BooleanField(
        default=False
    )

    # Calculates a team's Pontoon score based on completed fixtures.
    def calculate_score(self):

        if not self.team:
            return 0

        score = 0

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

            if fixture.home_team == self.team:

                score += (
                    fixture.home_team_score * 2
                )

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

    # Updates the team's score and checks whether they are bust.
    def update_score(self):
        self.score = self.calculate_score()

        if self.score > 21:
            self.busted = True
        else:
            self.busted = False

        self.save()

    def __str__(self):
        return f"Football {self.number}"


# Updates scores for all Pontoon teams.
def update_all_pontoon_scores():
    for ball in PontoonBall.objects.all():
        ball.update_score()


# Stores payment and access information for Pontoon users.
class PontoonAccess(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="pontoon_access"
    )

    has_access = models.BooleanField(default=False)

    stripe_pid = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    amount_paid = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} Pontoon Access"