from django.urls import path
from .views import (
    UserProfileRetrieveDetailAPIView, UserProfileRetrieveAPIView,
    FollowUserCreateAPIView, FollowersListAPIView,
    UsersAuthorIsFollowing, FollowUserDestroyAPIView)

get_profiles = path(
    'profiles/', UserProfileRetrieveAPIView.as_view(), name="get_profiles")
get_profile = path('profiles/<profile_username>',
                   UserProfileRetrieveDetailAPIView.as_view(), name="get_profile")
follow_user = path('profiles/<username>/follow',
                   FollowUserCreateAPIView.as_view(), name="follow_user")
list_of_user_followers = path('profiles/<username>/followers',
                              FollowersListAPIView.as_view(), name="list_of_user_followers")
list_of_users_author_is_following = path(
    'profiles/<username>/following', UsersAuthorIsFollowing.as_view(), name="list_of_users_author_is_following")
unfollow_user = path('profiles/<username>/unfollow',
                     FollowUserDestroyAPIView.as_view(), name="unfollow_user")
urlpatterns = [
    get_profiles,
    get_profile,
    follow_user,
    list_of_user_followers,
    list_of_users_author_is_following,
    unfollow_user,
]
