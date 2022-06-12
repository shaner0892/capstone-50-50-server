"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.city import City


class CityView(ViewSet):
    """50/50 city view"""

    def list(self, request):
        """Handle GET requests to get all cities

        Returns:
            Response -- JSON serialized list of cities
        """
        cities = City.objects.order_by('name')
        state = request.query_params.get('state', None)
        
        # return only the cities that are in the state the user chose
        if state is not None:
            cities = cities.filter(state__id=state)
        
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        city = City.objects.get(pk=pk)
        serializer = CitySerializer(city)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized city instance
        """
        serializer = CreateCitySerializer(data=request.data)
        # raise_exception=true will send error if user doesn't enter correct data/the data that you set in the serializer
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a city

        Returns:
            Response -- Empty body with 204 status code
        """

        city = City.objects.get(pk=pk)
        city.name = request.data["name"]
        city.state = request.data["state"]
        city.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        city = City.objects.get(pk=pk)
        city.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class CitySerializer(serializers.ModelSerializer):
    
    """JSON serializer for cities
    """
    class Meta:
        model = City
        fields = ('id', 'name', 'state')
        depth = 1
        
class CreateCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'state']
