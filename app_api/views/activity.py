"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.activity import Activity


class ActivityView(ViewSet):
    """50/50 activity view"""

    def list(self, request):
        """Handle GET requests to get all activities

        Returns:
            Response -- JSON serialized list of activities
        """
        activities = Activity.objects.filter(is_approved=True)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        """Handle GET requests for single activity

        Returns:
            Response -- JSON serialized activity
        """
        activity = Activity.objects.get(pk=pk)
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized activity instance
        """
        serializer = CreateActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def update(self, request, pk):
        """Handle PUT requests for an activity

        Returns:
            Response -- Empty body with 204 status code
        """
        activity = Activity.objects.get(pk=pk)
        activity.title = request.data["title"]
        activity.state = request.data["state"]
        activity.city = request.data["city"]
        activity.specific_location = request.data["specific_location"]
        activity.category = request.data["end_date"]
        activity.is_approved = request.data["is_approved"]
        # add rating
        activity.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        activity = Activity.objects.get(pk=pk)
        activity.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class ActivitySerializer(serializers.ModelSerializer):
    
    """JSON serializer for activities
    """
    class Meta:
        model = Activity
        fields = ('id', 'title', 'state', 'city', 'specific_location', 'category', 'is_approved')
        depth = 1
        
class CreateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'state', 'city', 'specific_location', 'category', 'is_approved']
