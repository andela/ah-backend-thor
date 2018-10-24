from rest_framework import status
from rest_framework import generics 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .backends import JWTAuthentication
import jwt
import sendgrid
from authors.settings import SENDGRID_API_KEY, SECRET_KEY


from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, PasswordSerializer
)
from .models import User

def generate_reset_token(data):
        token = jwt.encode({
            'email': data
        }, SECRET_KEY, algorithm='HS256')

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
    authentication_classes = (JWTAuthentication,)
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
      
class ResetPasswordAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (JWTAuthentication,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        #get user data
        user_data = request.data['user']['email']

        token = generate_reset_token(user_data)
        try:
            sg = sendgrid.SendGridAPIClient(apikey = SENDGRID_API_KEY)

            data = {
                "personalizations": [
                    {
                        "to": [{'email':user_data}],
                        "subject": "Password reset"
                    }
                    ],
                    "from": {
                        "email": user_data},
                    "content": [ 
                        {
                            "type": "text/plain",
                            "value": 'Follow this link to reset your passwword: http://localhost:8000/api/users/update_password/{}'.format(token)
                            }
                        ]
                }
            sg.client.mail.send.post(request_body=data)
            return Response({'message':'Check email to reset link', "token":token}, status=status.HTTP_201_CREATED)
            
        except:
            return Response({'message':'User doesnot exist'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (AllowAny,)
    # authentication_classes = (JWTAuthentication,)
    serializer_class = PasswordSerializer
    look_url_kwarg = 'token'

    def update(self, request, *args, **kwargs):
        #get token
        try:
            token = self.kwargs.get(self.look_url_kwarg)
            new_password = request.data.get('new_password')
            if not new_password:
                return Response({"message":"wrong input password"}, status=status.HTTP_400_BAD_REQUEST)
            decode_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(email=decode_token['email'])
            
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'message':'Update failed'}, status=status.HTTP_400_BAD_REQUEST)

        
