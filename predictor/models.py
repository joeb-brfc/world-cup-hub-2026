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