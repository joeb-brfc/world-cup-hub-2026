from django.db import models
from django.contrib.auth.models import User
from predictor.models import Team


class PontoonBall(models.Model):
    number = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return f"Football {self.number}"
    
    team = models.ForeignKey(
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