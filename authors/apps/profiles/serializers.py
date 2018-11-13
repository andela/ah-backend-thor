from rest_framework import serializers
from .models import Profile, FollowUser
from authors.apps.authentication.serializers import UserSerializer
from rest_framework.validators import UniqueTogetherValidator


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
        exclude = ['id']


class FollowUserSerializer(serializers.ModelSerializer):
    # add vaildation here
    def validate(self, data):
        following_username = data.get('following_username')
        followed_username = data.get('followed_username')

        if following_username is None:
            raise serializers.ValidationError(
                'Authentication credentials required.'
            )
        if followed_username is None:
            raise serializers.ValidationError(
                'URL username missing'
            )
        if following_username == followed_username:
            raise serializers.ValidationError(
                'You can not follow yourself!'
            )

        return {
            "following_username": following_username,
            "followed_username": followed_username
        }

    class Meta:
        model = FollowUser
        fields = ('followed_username', 'following_username')
        validators = [
            UniqueTogetherValidator(
                queryset=FollowUser.objects.all(),
                fields=('followed_username', 'following_username'),
                message="You are already following this user"
            )
        ]

    def create(self, validated_data):
        follow_user = FollowUser.objects.create(**validated_data)
        return follow_user
