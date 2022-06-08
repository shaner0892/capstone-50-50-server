from django.db import models

class RateReview(models.Model):

    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)
    rating = models.IntegerField()
    review = models.CharField(max_length=500)
    fifty_user = models.ForeignKey("FiftyUser", on_delete=models.CASCADE)
    date = models.DateField()
