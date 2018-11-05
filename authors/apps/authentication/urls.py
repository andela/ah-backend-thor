from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailVerification,
    SendPasswordResetEmailAPIView, PasswordUpdateAPIView
)

urlpatterns = [

    path('user/', UserRetrieveUpdateAPIView.as_view(), name='get_edit_user'),
    path('users/', RegistrationAPIView.as_view(), name='create_user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/update/<pk>', EmailVerification.as_view(), name="email_verification"),
    path('users/password_reset/', SendPasswordResetEmailAPIView.as_view(), name="send_password_reset_email"),
    path('users/update_password/<token>', PasswordUpdateAPIView.as_view(), name = "update_password"),

]
