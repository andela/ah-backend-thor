from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
from django.core.mail import send_mail

import sendgrid
import os
from sendgrid.helpers.mail import *

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import User
 

class RegistrationAPIView(generics.CreateAPIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        body = "click this link to verify your account   http://localhost:8000/api/users/update/{}".format(serializer.data['token'])
        email = serializer.data['email']
        send_mail('subject', body, 'andelateamthor@gmail.com', [email], fail_silently=False)
        return_data = serializer.data
        return_data.pop('token')
        return Response({'message': 'User successfully Registered'}, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        
        message = {
            'user_message':"User successfully confirmed",
            'user_token':serializer.data['token']
        }
        return Response(message, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class EmailVerification(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        email_token = jwt.decode(self.kwargs["pk"], settings.SECRET_KEY, algorithm='HS256')
        queryset = User.objects.filter(id=email_token['id'])
        User.objects.filter(id=email_token['id']).update(is_active=True)
        
        return queryset
    serializer_class = UserSerializer

