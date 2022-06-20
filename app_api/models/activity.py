from django.db import models

class Activity(models.Model):

    title = models.CharField(max_length=50)
    state = models.ForeignKey("State", on_delete=models.CASCADE)
    city = models.CharField(max_length=20)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    is_approved = models.BooleanField()
    
    @property
    def average_rating(self):
        """Average rating calculated attribute for each activity
        Returns:
            number -- The average rating for the activity
        """
        total_rating = 0
        try:
            for rating in self.ratings.all():
                total_rating += rating.rating

            avg = total_rating / self.ratings.count()
            return avg
        except: 
            return "No ratings yet"