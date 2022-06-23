"""View module for handling requests about states"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
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
    
    def update(self, request, pk):
        """Handle PUT requests for a state

        Returns:
            Response -- Empty body with 204 status code
        """
        state = State.objects.get(pk=pk)
        state.name = request.data["name"]
        state.postal_abbreviation = request.data["postal_abbreviation"]
        state.capital = request.data["capital"]
        state.established = request.data["established"]
        state.population = request.data["population"]
        state.flag_url = request.data["flag_url"]
        state.largest_city = request.data["largest_city"]
        state.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class StateSerializer(serializers.ModelSerializer):
    
    """JSON serializer for states
    """
    class Meta:
        model = State
        fields = ('id', 'name', 'postal_abbreviation', 'capital', 'established', 'population', 'flag_url', 'largest_city')
        depth = 1
        