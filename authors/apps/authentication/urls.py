from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
<<<<<<< HEAD
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='get_edit_user'),
    path('users/', RegistrationAPIView.as_view(), name='create_user'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
=======
    path('user/', UserRetrieveUpdateAPIView.as_view()),
    path('users/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
>>>>>>> Revert "Develop (#13)" (#15)
]
