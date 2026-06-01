from django.db import models
from django.contrib.auth.models import User
from predictor.models import Team


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
        """
        Placeholder score calculation.
        Will be updated later to use fixture results.
        """
        return 0
    
    def update_score(self):
        self.score = self.calculate_score()
        if self.score > 21:
            self.busted = True
        else:
            self.busted = False
        self.save()
    
    def __str__(self):
        return f"Football {self.number}"