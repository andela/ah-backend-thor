from rest_framework import serializers
from .models import Profile
from authors.apps.authentication.serializers import UserSerializer

class CustomUserSerializer(serializers.RelatedField):
    """Custom Serializer to Get a name"""
    def to_representation(self, value):
        return value.username

    def get_queryset(self):
        pass

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for User Profile"""
    profile_user = CustomUserSerializer()

    class Meta:
        model = Profile
        feilds = ('profile_user', 'bio', 'image', 'following')
        exclude =['id']
