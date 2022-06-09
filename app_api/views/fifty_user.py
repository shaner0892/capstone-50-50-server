"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.trip import Trip
from app_api.models.fifty_user import FiftyUser


class FiftyUserView(ViewSet):
    """50/50 user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user

        Returns:
            Response -- JSON serialized user
        """
        fifty_user = FiftyUser.objects.get(pk=pk)
        serializer = FiftyUserSerializer(fifty_user)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of all users
        """
        fifty_users = FiftyUser.objects.all()
        serializer = FiftyUserSerializer(fifty_users, many=True)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a user

        Returns:
            Response -- Empty body with 204 status code
        """

        fifty_user = FiftyUser.objects.get(pk=pk)
        user = User.objects.get(pk=fifty_user.user_id)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.username = request.data["username"]
        user.email = request.data["email"]
        user.save()
        fifty_user.location = request.data["location"]
        fifty_user.bio = request.data["bio"]
        fifty_user.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class FiftyUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FiftyUser
        fields = ('id', 'bio', 'location', 'user')
        depth = 2