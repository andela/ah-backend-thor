from django.test import TestCase
from ..backends import JWTAuthentication
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import request, authentication, exceptions
from ..models import User

class JwtTestCase( JWTAuthentication, TestCase):
    '''Test JWT authentication for authors-haven'''
    
    def setUp(self):
        """Define the test client and other test variables."""

        self.client = APIClient()
        self.uri = '/api/users/'
        self.uri2 = '/api/users/login/'
        self.uri3 = 'api/user/'
        
        self.params1 = {
            "user": {
                "email": "kegz@gmail.com",
                "username": "kegz",
                "password": "1231234567"
            }
        }
        self.params2 = {
            "user": {
                "email": "kegz@gmail.com",
                "password": "1231234567"
            }
        }
        self.response = self.client.post(self.uri, self.params1, format='json')
        User.objects.filter(email='kegz@gmail.com').update(is_active=True)
        self.response2 = self.client.post(self.uri2, self.params2, format='json')
        self.response3 = self.client.get(self.uri3, self.params2, format='json')
        self.token = self.response2.data['token']
       

    def test_auth_header_prefix(self):
        self.assertEqual('Token', self.authentication_header_prefix)

    def test_user_can_get_token(self):
        
        self.assertEqual(201, self.response.status_code)
        self.assertIn('token', self.response2.data)
        self.assertTrue('token' not in self.response.data)

    def test_authenticate_credentials(self):
        resp = self._authenticate_credentials(request, self.token)
        
        self.assertTrue(isinstance(resp[0],User))
        self.assertTrue(isinstance(resp[1], str))

    def test_authenticate(self):
        resp = self.authenticate
        self.assertTrue(resp != None )

    def test_user_can_get_current_user(self):
        self.assertTrue(201, self.response3.status_code)
