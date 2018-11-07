from rest_framework import status
from rest_framework import generics 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.core.mail import send_mail
from django.conf import settings

from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, PasswordSerializer
)
from django.core.mail import send_mail

import sendgrid
import os


import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import User


from .models import User
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.social_serializers import TwitterLoginSerializer
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
import facebook

def generate_password_reset_token(data):
        token = jwt.encode({
            'email': data
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


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
        subject = "Hi {}".format(serializer.data['username'])
        body = "click this link to verify your account   http://localhost:8000/api/users/update/{}".format(
            serializer.data['token'])
        email = serializer.data['email']
        send_mail(subject, body, os.getenv("EMAIL"),
                  [email], fail_silently=False)
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
            'user_message': "User successfully confirmed",
            'user_token': serializer.data['token']
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
      
class SendPasswordResetEmailAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def post(self, request):
        #get user email
        user_data = request.data['user']['email']

        if not user_data:
            return Response({"message":"Please fill in your email"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_email = User.objects.get(email=user_data)

            token = generate_password_reset_token(user_data)

            from_email = user_email
            to_email = [user_email]
            subject = "Password Reset Email Link"
            message = "Follow this link to reset your passwword: http://localhost:8000/api/users/update_password/{}".format(token)

            send_mail(subject, message, from_email, to_email, fail_silently= False)
            return Response(
                {'message':'Check your email for the password reset link', "token":token}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message':'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            

class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordSerializer
    look_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        #get token
        token = self.kwargs.get(self.look_url_kwarg)
        new_password = request.data.get('new_password')

        if not new_password:
            return Response({"message":"Please fill in your password"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=decode_token['email'])
            
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message':'Update failed'}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerification(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        email_token = jwt.decode(
            self.kwargs["pk"], settings.SECRET_KEY, algorithm='HS256')
        queryset = User.objects.filter(id=email_token['id'])
        User.objects.filter(id=email_token['id']).update(is_active=True)

        return queryset
    serializer_class = UserSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    client_class = OAuth2Client
    # serializer_class = SocialRegisterSerializer
    # renderer_classes = (UserJSONRenderer,)

    # def post(self, request):
    #     data = json.loads(request.body.decode('utf-8'))
    #     access_token = data.get('access_token')
    #     try:
    #         faceBookGraphApiExplorer = facebook.GraphAPI(access_token=access_token)
    #         user_info = graph.get_object(
    #             id='me',
    #             fields='email, middle_name, last_name,'
    #             'first_name')
    #     except facebook.GraphAPIError:
    #         return JsonResponse({'error': 'Invalid data'}, safe=False)
    #     try:
    #         user = User.objects.get(facebook_email=user_info.get('email'))
    #     except User.DoesNotExist:
    #         password = User.objects.make_random_password()
    #         pass


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
