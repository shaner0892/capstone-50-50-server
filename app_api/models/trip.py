from django.db import models

class Trip(models.Model):

    fifty_user = models.ForeignKey("FiftyUser", on_delete=models.CASCADE, related_name="trips")
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    about = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField()
    rating = models.IntegerField()
    activities = models.ManyToManyField("Activity", related_name="trips")
    
    # for stretch goal state and city will become a many-to-many because they can visit multiple cities and states in one trip