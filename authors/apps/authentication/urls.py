from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, ResetPasswordAPIView, PasswordUpdateAPIView
)

urlpatterns = [

    path('user/', UserRetrieveUpdateAPIView.as_view(), name='get_edit_user'),
    path('users/', RegistrationAPIView.as_view(), name='create_user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/password_reset/', ResetPasswordAPIView.as_view()),
    path('users/update_password/<token>', PasswordUpdateAPIView.as_view()),

]
