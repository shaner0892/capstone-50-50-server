from django.db import models

class Activity(models.Model):

    title = models.CharField(max_length=50)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    specific_location = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    is_approved = models.BooleanField()
    