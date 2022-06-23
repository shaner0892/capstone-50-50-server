"""View module for handling requests about reviews"""
from datetime import date
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from app_api.models.rate_review import RateReview
from app_api.models.fifty_user import FiftyUser


class ReviewView(ViewSet):
    """50/50 review view"""

    def list(self, request):
        """Handle GET requests to get all reviews

        Returns:
            Response -- JSON serialized list of reviews
        """
        activity = self.request.query_params.get("activity", None)
        reviews = RateReview.objects.filter(activity_id=activity)           
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        """Handle GET requests for single review

        Returns:
            Response -- JSON serialized review
        """
        review = RateReview.objects.get(pk=pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized review instance
        """
        fifty_user = FiftyUser.objects.get(user=request.auth.user)
        today = date.today()
        serializer = CreateReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(fifty_user=fifty_user, date=today)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    def destroy(self, request, pk):
        review = RateReview.objects.get(pk=pk)
        review.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

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
