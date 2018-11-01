from django.test import TestCase
from ..backends import JWTAuthentication
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import request, authentication, exceptions
from ..models import User


class JwtTestCase(JWTAuthentication, TestCase):
    '''Test JWT authentication for authors-haven'''

    def setUp(self):
        """Define the test client and other test variables."""

        self.client = APIClient()
        self.register_url = '/api/users/'
        self.login_url = '/api/users/login/'
        self.get_user_url = '/api/user/'

        self.user = {
            "user": {
                "username": "dude",
                "email": "dude1@gmail.com",
                "password": "password"
            }
        }

        self.response = self.client.post(
            self.register_url, self.user, format='json')
        self.user_login = self.client.post(
            self.login_url, self.user, format='json')

    def test_auth_header_prefix(self):
        self.assertEqual('Token', self.authentication_header_prefix)

    def test_user_can_get_token(self):
        self.assertEqual(201, self.response.status_code)
        self.assertIn('user_token', self.user_login.data)

    def test_authenticate_credentials(self):
        self.token = self.user_login.data['user_token']
        resp = self._authenticate_credentials(request, self.token)

    def test_authenticate(self):
        resp = self.authenticate
        self.assertTrue(resp != None)
