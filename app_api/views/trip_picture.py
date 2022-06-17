"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.trip import Trip
from app_api.models.trip_picture import TripPicture

class TripPictureView(ViewSet):
    """50/50 trip pictures view"""

    def list(self, request):
        """Handle GET requests to get all pictures for a trip

        Returns:
            Response -- JSON serialized list of trip pictures
        """
        # need to filter so only pictures for a single trip return
        trip = self.request.query_params.get("trip", None)
        trip_pictures = TripPicture.objects.filter(trip_id=trip)
        serializer = TripPictureSerializer(trip_pictures, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for a single trip picture

        Returns:
            Response -- JSON serialized trip picture
        """
        trip_picture = TripPicture.objects.get(pk=pk)
        serializer = TripPictureSerializer(trip_picture)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized trip picture
        """
        trip = Trip.objects.get(pk=request.data["trip"])
        serializer = CreateTripPictureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(trip=trip)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def update(self, request, pk):
        """Handle PUT requests for a trip picture

        Returns:
            Response -- Empty body with 204 status code
        """

        trip_picture = TripPicture.objects.get(pk=pk)
        trip = Trip.objects.get(pk=request.data["trip"])
        # trip_picture.picture_url.add(*request.data["picture_url"])
        trip_picture.url = request.data["url"]
        trip_picture.save(trip=trip)
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        trip_picture = TripPicture.objects.get(pk=pk)
        trip_picture.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
        
class TripPictureSerializer(serializers.ModelSerializer):
    
    """JSON serializer for trip pictures
    """
    
    class Meta:
        model = TripPicture
        fields = ('url',)
        depth = 1
        
class CreateTripPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripPicture
        fields = ['id', 'trip', 'url']
