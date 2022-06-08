from django.db import models

class Activity(models.Model):

    title = models.CharField(max_length=50)
    city = models.ForeignKey("City", on_delete=models.CASCADE)
    specific_location = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    is_approved = models.BooleanField()
    