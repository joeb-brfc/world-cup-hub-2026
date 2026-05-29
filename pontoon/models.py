from django.db import models
from django.contrib.auth.models import User
from predictor.models import Team


class PontoonBall(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Football {self.number}"