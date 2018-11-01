from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer
)
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
        
        self.send(serializer.data['email'], serializer.data['token'])
        return_data = serializer.data
        return_data.pop('token')
        return Response(return_data, status=status.HTTP_201_CREATED)
    
    def send(self, user_email, email_token):
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("john.kalyango@andela.com")
        to_email = Email(user_email)
        subject = "You have successfully"
        content = Content("text/plain", "and easy to do anywhere, even with Python   http://localhost:8000/api/users/update/{}".format(email_token))
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)

<<<<<<< HEAD
=======
        self.send(serializer.data['email'], serializer.data['token'])
        return_data = serializer.data
        return_data.pop('token')
        return Response(return_data, status=status.HTTP_201_CREATED)
    
    def send(self, user_email, email_token):
        sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("john.kalyango@andela.com")
        to_email = Email(user_email)
        subject = "You have successfully"
        content = Content("text/plain", "and easy to do anywhere, even with Python   http://localhost:8000/api/users/update/{}".format(email_token))
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
>>>>>>> 40b63aa5d14eb8860bfb4d57628c3c53bae6ccf8


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
        
        return Response(serializer.data, status=status.HTTP_200_OK)


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

