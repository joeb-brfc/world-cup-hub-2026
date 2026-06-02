from django.db import models
from django.contrib.auth.models import User
from predictor.models import Team
from predictor.models import Fixture


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
            if (
                fixture.home_team_score is None
                or
                fixture.away_team_score is None
            ):
                continue

            if fixture.home_team == self.team:
                score += fixture.home_team_score * 2
                score -= fixture.away_team_score
            else:
                score += fixture.away_team_score * 2
                score -= fixture.home_team_score

        return score
    
    def update_score(self):
        self.score = self.calculate_score()
        if self.score > 21:
            self.busted = True
        else:
            self.busted = False
        self.save()
    
    def __str__(self):
        return f"Football {self.number}"