from django.db import models

class State(models.Model):

    name = models.CharField(max_length=50)
    postal_abbreviation = models.CharField(max_length=2)
    capital = models.CharField(max_length=50)
    established = models.CharField(max_length=20)
    population = models.IntegerField()
    flag_url = models.CharField(max_length=1000)
    largest_city = models.CharField(max_length=50)
    
    # add a custom property of best_activities for each state
