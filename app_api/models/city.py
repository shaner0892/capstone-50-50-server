from django.db import models

class City(models.Model):

    name = models.CharField(max_length=50)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    
