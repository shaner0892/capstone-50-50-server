"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.category import Category


class CategoryView(ViewSet):
    """50/50 category view"""

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # def retrieve(self, request, pk):
    #     """Handle GET requests for single trip

    #     Returns:
    #         Response -- JSON serialized trip
    #     """
    #     trip = Trip.objects.get(pk=pk)
    #     serializer = TripSerializer(trip)
    #     return Response(serializer.data)
    
    # def create(self, request):
    #     """Handle POST operations

    #     Returns
    #         Response -- JSON serialized game instance
    #     """
    #     fifty_user = FiftyUser.objects.get(user=request.auth.user)
    #     serializer = CreateTripSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(fifty_user=fifty_user)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    # def update(self, request, pk):
    #     """Handle PUT requests for a game

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """

    #     trip = Trip.objects.get(pk=pk)
    #     trip.state = request.data["state"]
    #     trip.city = request.data["city"]
    #     trip.about = request.data["about"]
    #     trip.start_date = request.data["start_date"]
    #     trip.end_date = request.data["end_date"]
    #     trip.completed = request.data["completed"]
    #     # add rating
    #     trip.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    # def destroy(self, request, pk):
    #     game = Trip.objects.get(pk=pk)
    #     game.delete()
    #     return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class CategorySerializer(serializers.ModelSerializer):
    
    """JSON serializer for categories
    """
    class Meta:
        model = Category
        fields = ('id', 'name')
        depth = 1
        
# class CreateTripSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trip
#         fields = ['id', 'state', 'city', 'about', 'start_date', 'end_date', 'completed']
