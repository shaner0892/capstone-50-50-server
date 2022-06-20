"""View module for handling requests about game types"""
from datetime import date
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.rate_review import RateReview
from app_api.models.trip import Trip
from app_api.models.state import State
from app_api.models.fifty_user import FiftyUser


class ReviewView(ViewSet):
    """50/50 trips view"""

    def list(self, request):
        """Handle GET requests to get all trips

        Returns:
            Response -- JSON serialized list of trips filtered by user
        """
        activity = self.request.query_params.get("activity", None)
        reviews = RateReview.objects.filter(activity_id=activity)           
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized trip
        """
        review = RateReview.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized trip instance
        """
        fifty_user = FiftyUser.objects.get(user=request.auth.user)
        today = date.today()
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(fifty_user=fifty_user, date=today)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # def update(self, request, pk):
    #     """Handle PUT requests for a trip

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """

    #     trip = Trip.objects.get(pk=pk)
    #     state = State.objects.get(pk=request.data["state"])
    #     trip.state = state
    #     trip.city = request.data["city"]
    #     trip.about = request.data["about"]
    #     trip.start_date = request.data["start_date"]
    #     trip.end_date = request.data["end_date"]
    #     trip.completed = request.data["completed"]
    #     trip.activities.add(*request.data["activity"])
    #     trip.rating = request.data["rating"]
    #     trip.save()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        review = RateReview.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    # @action(methods=["get"], detail=False)
    # def my_trips(self, request):
    #     user = FiftyUser.objects.get(user=request.auth.user)
    #     # (user on the left side is the property on trip you are referring to, 
    #     # user on the right is the one you just defined that you want to compare it to)
    #     trips = Trip.objects.filter(fifty_user=user)
    #     serializer = TripSerializer(trips, many=True)
    #     return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class FiftyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FiftyUser
        fields = ('id', 'bio', 'user')
        
class ReviewSerializer(serializers.ModelSerializer):
    
    """JSON serializer for reviews
    """
    fifty_user = FiftyUserSerializer()
    
    class Meta:
        model = RateReview
        fields = ('id', 'activity', 'rating', 'review', 'fifty_user')
        depth = 1
        
class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateReview
        fields = ['id', 'activity', 'rating', 'review']
