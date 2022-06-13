from django.db import models
from django.contrib.auth.models import User

class FiftyUser(models.Model):

    bio = models.CharField(max_length=300)
    image_url = models.CharField(max_length=1000)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # add a custom property to include the states each user has visited
    @property
    def states_visited(self):
        states = []
        for trip in self.trips.all():
            states.append(trip.state)
        return states