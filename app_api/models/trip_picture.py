from django.db import models

class TripPicture(models.Model):

    trip = models.ForeignKey("Trip", on_delete=models.CASCADE)
    picture_url = models.CharField(max_length=1000)
    