from django.db import models

class Trip(models.Model):

    fifty_user = models.ForeignKey("FiftyUser", on_delete=models.CASCADE)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    about = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField()
    rating = models.IntegerField()
    
    # for stretch goal state and city will become a many-to-many because they can visit multiple cities and states in one trip