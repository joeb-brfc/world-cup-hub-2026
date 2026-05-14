from django.db import models

# Create your models here.
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
    best_world_cup_year = models.PositiveIntegerField(blank=True, null=True)    

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
    kickoff_time = models.DateTimeField()
    home_team_score = models.PositiveIntegerField(blank=True, null=True)
    away_team_score = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        ordering = ['kickoff_time']

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
