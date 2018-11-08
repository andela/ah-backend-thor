from django.urls import path
from .views import UserProfileRetrieveDetailAPIView, UserProfileRetrieveAPIView

urlpatterns = [
    path('profiles/', UserProfileRetrieveAPIView.as_view(), name="get_profiles"),
    path('profiles/<profile_user_id>', UserProfileRetrieveDetailAPIView.as_view(), name="get_profile")
    
]


