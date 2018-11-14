from django.urls import path
from .views import (
    UserProfileRetrieveDetailAPIView, UserProfileRetrieveAPIView, 
    FollowUserCreateAPIView, FollowersListAPIView,
    UsersAuthorIsFollowing, FollowUserDestroyAPIView)

urlpatterns = [
    path('profiles/', UserProfileRetrieveAPIView.as_view(), name="get_profiles"),
    path('profiles/<profile_username>', UserProfileRetrieveDetailAPIView.as_view(), name="get_profile"),
    path('profiles/<username>/follow', FollowUserCreateAPIView.as_view(), name ="follow_user"),
    path('profiles/<username>/followers', FollowersListAPIView.as_view(), name ="list_of_user_followers"),
    path('profiles/<username>/following', UsersAuthorIsFollowing.as_view(), name ="list_of_users_author_is_following"),
    path('profiles/<username>/unfollow', FollowUserDestroyAPIView.as_view(), name ="unfollow_user"), 
]

