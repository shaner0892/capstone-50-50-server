"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.state import State


class StateView(ViewSet):
    """50/50 state view"""

    def list(self, request):
        """Handle GET requests to get all states

        Returns:
            Response -- JSON serialized list of states
        """
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single state

        Returns:
            Response -- JSON serialized state
        """
        state = State.objects.get(pk=pk)
        serializer = StateSerializer(state)
        return Response(serializer.data)
    

class StateSerializer(serializers.ModelSerializer):
    
    """JSON serializer for states
    """
    class Meta:
        model = State
        fields = ('id', 'name', 'postal_abbreviation', 'capital', 'established', 'population', 'flag_url', 'largest_city')
        depth = 1
        
# class CreateTripSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Trip
#         fields = ['id', 'state', 'city', 'about', 'start_date', 'end_date', 'completed']
