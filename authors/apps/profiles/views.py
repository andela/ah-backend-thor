
import jwt, os

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from .serializers import UserProfileSerializer, FollowUserSerializer
from .models import Profile, FollowUser
from .renderers import ProfileRenderer
from authors.apps.authentication.models import User
from rest_framework.permissions import IsAuthenticated
from django.views.generic.edit import UpdateView
from authors.apps.authentication.backends import JWTAuthentication
from rest_framework.exceptions import APIException
from django.conf import settings
from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ArticleSerializer


def token_payload(request):
    token = request.META.get('HTTP_AUTHORIZATION', ' ').split(' ')[1]
    decode_token = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
    following_user_id = decode_token['id']
    following_user = User.objects.get(pk=following_user_id)
    following_username = following_user.username
    return following_username


class UserProfileRetrieveDetailAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_classfollow = FollowUserSerializer

    def get_queryset(self):
        QuerySet = Profile.objects.filter(
            profile_user__username=self.kwargs["profile_username"])  # pragma: no cover
        return QuerySet  # pragma: no cover

    renderer_classes = (ProfileRenderer,)
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):

        followed_user_username = self.kwargs["profile_username"]

        following_username = token_payload(request)
        following_user_instances = FollowUser.objects.filter(
            following_username=following_username)
        try:
            user_profile = Profile.objects.get(
                profile_user__username=followed_user_username)
            for user_instance in following_user_instances:
                if user_instance.followed_username == followed_user_username:
                    user_profile.following = True
            serializer = self.serializer_class(user_profile)

            return Response({
                "user": serializer.data
            },
                status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            raise APIException({
                'error': 'User does not exist'
            })


class UserProfileRetrieveAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    renderer_classes = (ProfileRenderer,)
    serializer_class = UserProfileSerializer


class FollowUserCreateAPIView(generics.CreateAPIView):
    """ Creates an instance of a user following another user"""
    authentication_class = (JWTAuthentication,)
    permission_class = (IsAuthenticated,)
    serializer_class = FollowUserSerializer
    serializer_classprofile = UserProfileSerializer
    serializer_classarticle = ArticleSerializer
    look_url_kwarg = 'username'

    def post(self, request, *args, **kwargs):
        """ Allow a user to follow other users """
        user_articles = []

        following_username = token_payload(request)

        followed_username = self.kwargs.get(self.look_url_kwarg)
        try:
            followed_user = User.objects.get(username=followed_username)

            serializer = self.serializer_class(
                data={
                    "following_username": following_username,
                    "followed_username": followed_username
                })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # bio of followed_user
            followed_user_id = followed_user.id
            followed_user_profile = Profile.objects.get(
                profile_user=followed_user_id)
            serializer_profile = self.serializer_classprofile(
                followed_user_profile)

            # articles of followed user
            followed_user_articles = Article.objects.filter(
                author=followed_user_id)

            for article in followed_user_articles:
                serializer_article = self.serializer_classarticle(
                    article)  # pragma: no cover

            return Response({
                "following_user": following_username,
                "followed_user": serializer_profile.data,
                "followed_articles": user_articles
            },
                status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            raise APIException({
                'error': 'User does not exist'
            })


class FollowersListAPIView(generics.ListAPIView):
    """ Returns all the users that are follow the author"""
    serializer_class = FollowUserSerializer
    serializer_classprofile = UserProfileSerializer
    look_url_kwarg = 'username'

    def get_queryset(self, *args, **kwargs):
        followed_username = self.kwargs.get(self.look_url_kwarg)
        followers = FollowUser.objects.filter(
            followed_username=followed_username)

        return followers


class FollowUserDestroyAPIView(generics.DestroyAPIView):
    """ Allows the user to unfollow another user"""
    authentication_class = (JWTAuthentication,)
    permission_class = (IsAuthenticated,)
    serializer_class = FollowUserSerializer
    serializer_classprofile = UserProfileSerializer
    look_url_kwarg = 'username'

    def delete(self, request, *args, **kwargs):
        """ Allow a user to unfollow another user"""

        following_username = token_payload(request)

        followed_username = self.kwargs.get(self.look_url_kwarg)
        try:
            followed_user = User.objects.get(username=followed_username)
            followed_user_id = followed_user.id

            is_following = FollowUser.objects.filter(
                following_username=following_username)
            for user in is_following:
                if user.following_username == following_username and user.followed_username == followed_username:
                    returned_user = FollowUser.objects.get(pk=user.id)
                    returned_user.delete()

                    followed_user_profile = Profile.objects.get(
                        profile_user=followed_user_id)
                    serializer_profile = self.serializer_classprofile(
                        followed_user_profile)
                    return Response({
                        "user": following_username,
                        "unfollowing": serializer_profile.data
                    })
            return Response({
                "message": 'User has been unfollowed or You are unfollowing a user you were not orignally following'
            }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "message": 'User does not exist'
            }, status=status.HTTP_400_BAD_REQUEST)


class UsersAuthorIsFollowing(generics.ListAPIView):
    """ All authors a user is following """
    serializer_class = FollowUserSerializer
    serializer_classprofile = UserProfileSerializer
    look_url_kwarg = 'username'

    def get_queryset(self, *args, **kwargs):
        """ All authors user is following"""
        following_username = self.kwargs.get(self.look_url_kwarg)
        following_users = FollowUser.objects.filter(
            following_username=following_username)

        return following_users
