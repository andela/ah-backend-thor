from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, EmailVerification
)

urlpatterns = [

<<<<<<< HEAD

=======
>>>>>>> b1cfef2... [feature #161382391] Send verification email upon login
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='get_edit_user'),
    path('users/', RegistrationAPIView.as_view(), name='create_user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/update/<pk>', EmailVerification.as_view(), name="email_verification"),

<<<<<<< HEAD

=======
>>>>>>> b1cfef2... [feature #161382391] Send verification email upon login
]
