"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.trip import Trip
from app_api.models.state import State
from app_api.models.fifty_user import FiftyUser


class TripView(ViewSet):
    """50/50 trips view"""

    def list(self, request):
        """Handle GET requests to get all trips

        Returns:
            Response -- JSON serialized list of trips filtered by user
        """
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single trip

        Returns:
            Response -- JSON serialized trip
        """
        trip = Trip.objects.get(pk=pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized trip instance
        """
        fifty_user = FiftyUser.objects.get(user=request.auth.user)
        rating = 0
        serializer = CreateTripSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(fifty_user=fifty_user, rating=rating)
        trip = Trip.objects.get(pk=serializer.data["id"])
        # here we are adding one activity at a time to the trip.activities array
        trip.activities.add(*request.data["activity"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def update(self, request, pk):
        """Handle PUT requests for a trip

        Returns:
            Response -- Empty body with 204 status code
        """

        trip = Trip.objects.get(pk=pk)
        state = State.objects.get(pk=request.data["state"])
        trip.state = state
        trip.city = request.data["city"]
        trip.about = request.data["about"]
        trip.start_date = request.data["start_date"]
        trip.end_date = request.data["end_date"]
        trip.completed = request.data["completed"]
        trip.activities.add(*request.data["activity"])
        # add rating
        trip.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        trip = Trip.objects.get(pk=pk)
        trip.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=["get"], detail=False)
    def my_trips(self, request):
        user = FiftyUser.objects.get(user=request.auth.user)
        # (user on the left side is the property on trip you are referring to, 
        # user on the right is the one you just defined that you want to compare it to)
        trips = Trip.objects.filter(fifty_user=user)
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')

class FiftyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FiftyUser
        fields = ('id', 'bio', 'user')
        
class TripSerializer(serializers.ModelSerializer):
    
    """JSON serializer for trips
    """
    fifty_user = FiftyUserSerializer()
    
    class Meta:
        model = Trip
        fields = ('id', 'state', 'city', 'about', 'start_date', 'end_date', 'completed', 'fifty_user', 'activities')
        depth = 1
        
class CreateTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'state', 'city', 'start_date', 'end_date', 'completed']
