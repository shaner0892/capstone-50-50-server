"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.activity import Activity
from app_api.models.state import State
from app_api.models.category import Category



class ActivityView(ViewSet):
    """50/50 activity view"""

    def list(self, request):
        """Handle GET requests to get all activities

        Returns:
            Response -- JSON serialized list of activities
        """
        # activities = Activity.objects.filter(is_approved=True)
        activities = Activity.objects.all()
        # user is able to filter by category or state, or sort by rating
        # request that info and apply selected filters, otherwise return all activities
        category = request.query_params.get('category', None) 
        state = request.query_params.get('state', None)
        rating = request.query_params.get('rating', None)               
        if category is not None:
            activities = activities.filter(category__id=category) 
        if state is not None:
            activities = activities.filter(state__id=state) 
        if rating is 1:
            activities = activities.order_by('average_rating')
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
        # the front end is only sending an id so you need to get the whole object for state and category
        state = State.objects.get(pk=request.data["state"])
        category = Category.objects.get(pk=request.data["category"])
        activity.title = request.data["title"]
        activity.state = state
        activity.city = request.data["city"]
        activity.category = category
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
        fields = ('id', 'title', 'state', 'city', 'category', 'is_approved', 'average_rating')
        depth = 1
        
class CreateActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'title', 'state', 'city', 'category', 'is_approved']
