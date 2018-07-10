from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailVerification
)

urlpatterns = [


    path('user/', UserRetrieveUpdateAPIView.as_view(), name='get_edit_user'),
    path('users/', RegistrationAPIView.as_view(), name='create_user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/update/<pk>', EmailVerification.as_view(), name="email_verification"),


]
