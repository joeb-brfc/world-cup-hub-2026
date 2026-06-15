from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Stadium(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    capacity = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
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

    name = models.CharField(max_length=100)
    group = models.CharField(max_length=1, choices=GROUP_CHOICES)
    manager = models.CharField(max_length=100, blank=True, null=True)
    captain = models.CharField(max_length=100, blank=True, null=True)
    best_world_cup_finish = models.CharField(max_length=100, blank=True, null=True)
    best_world_cup_year = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class Fixture(models.Model):
    STAGE_CHOICES = [
        ('Group Stage', 'Group Stage'),
        ('Round of 32', 'Round of 32'),
        ('Round of 16', 'Round of 16'),
        ('Quarterfinals', 'Quarterfinals'),
        ('Semifinals', 'Semifinals'),
        ('Final', 'Final'),
    ]

    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_fixtures'
    )

    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_fixtures'
    )

    stadium = models.ForeignKey(
        Stadium,
        on_delete=models.SET_NULL,
        related_name='fixtures',
        null=True,
        blank=True
    )

    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    matchday = models.PositiveIntegerField(
    blank=True,
    null=True
)
    kickoff_time = models.DateTimeField()
    home_team_score = models.PositiveIntegerField(blank=True, null=True)
    away_team_score = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['kickoff_time']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"

    def predictions_locked(self):
        lock_time = self.kickoff_time + timedelta(hours=1)
        return timezone.now() >= lock_time

    def update_prediction_points(self):
        predictions = self.predictions.all()

        for prediction in predictions:
            prediction.points_awarded = prediction.calculate_points()

            Prediction.objects.filter(id=prediction.id).update(
                points_awarded=prediction.points_awarded
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Recalculate prediction points when a fixture result is saved.
        self.update_prediction_points()

        # Recalculate Pontoon scores when a fixture result is saved.
        from pontoon.models import update_all_pontoon_scores
        update_all_pontoon_scores()


class Prediction(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    fixture = models.ForeignKey(
        Fixture,
        on_delete=models.CASCADE,
        related_name='predictions'
    )

    predicted_home_score = models.PositiveIntegerField()
    predicted_away_score = models.PositiveIntegerField()
    points_awarded = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fixture')
        ordering = ['fixture__kickoff_time']

    def __str__(self):
        return f"{self.user.username}'s prediction for {self.fixture}"

    def calculate_points(self):
        fixture = self.fixture

        if (
            fixture.home_team_score is None or
            fixture.away_team_score is None
        ):
            return 0

        # Exact score prediction = 3 points.
        if (
            self.predicted_home_score == fixture.home_team_score and
            self.predicted_away_score == fixture.away_team_score
        ):
            return 3

        # Correct match outcome = 1 point.
        predicted_difference = (
            self.predicted_home_score - self.predicted_away_score
        )

        actual_difference = (
            fixture.home_team_score - fixture.away_team_score
        )

        if predicted_difference > 0 and actual_difference > 0:
            return 1

        if predicted_difference < 0 and actual_difference < 0:
            return 1

        if predicted_difference == 0 and actual_difference == 0:
            return 1

        return 0

    def save(self, *args, **kwargs):
        self.points_awarded = self.calculate_points()
        super().save(*args, **kwargs)