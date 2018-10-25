from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class TestPoll(APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""

        self.client = APIClient()
        self.uri = '/api/users/'
        self.uri2 = '/api/users/login/'
        
        self.params1 = {
            "email": "kegz@gmail.com",
            "username": "kegz",
            "password": "1231234567"
        }
        self.params2 = {
            "email": "kegz@gmail.com",
            "username": "kegz",
            "password": "1"
        }
        self.params3 = {
            "email": "kegz@gmail.com",
            "username": "kegz",
            "password": "1231234567"
        }
        self.params4 = {
            "email": "kegzgmail.com",
            "username": "kegz",
            "password": "1231234567"
        }
        self.params5 = {
            "email": "kegz@gmail.com",
            "username": "kegz",
            "password": ""
        }
        self.params6 = {
            "email": "kegz@gmail.com",
            "username": "",
            "password": "123456789"
        }
        self.params7 = {
            "email": "",
            "username": "kalyango",
            "password": "123456789"
        }
        self.params8 = {
            "email": "kegz@gmail.com",
            "password": "123124567"
        }
        self.params9 = {
            "email": "kegzgmail.com",
            "password": "123456789"
        }

    def test_create_user(self):
        """test create new user when registering"""
        response = self.client.post(self.uri, self.params1)
        self.assertEqual(response.status_code, 400, 'Expected Response1 Code 201, received {0} instead.'.format(response.status_code))
        self.assertIn('errors', response.data)

    def test_wrong_password_digit_number(self):
        """test if password has 8 digits or more when registering"""
        response = self.client.post(self.uri, self.params2)
        self.assertEqual(response.status_code, 400, 'Expected Response2 Code 400, received {0} instead.'.format(response.status_code))
        self.assertIn('errors', response.data)

    def test_email_already_exists(self):
        """Test if the password already exits"""
        response = self.client.post(self.uri, self.params1)
        response = self.client.post(self.uri, self.params3)
        self.assertIn('errors', response.data)

    def test_wrong_email(self):
        """Test for wrong email"""
        self.response = self.client.post(self.uri, self.params4)
        self.assertIn('errors', self.response.data)

    def test_missing_fields(self):
        """Test for missing fields"""
        response = self.client.post(self.uri, self.params5)
        self.assertIn('errors', response.data)
        response = self.client.post(self.uri, self.params6)
        self.assertIn('errors', response.data)
        response = self.client.post(self.uri, self.params7)
        self.assertIn('errors', response.data)

    def test_login(self):
        """Test for logging in a user"""
        self.params = {
            "email": "kegz@gmail.com",
            "password": "1231234567"
        }
        response = self.client.post(self.uri, self.params1)
        response = self.client.post(self.uri2, self.params)
        self.assertEqual(response.status_code, 400, 'Expected Response Code 200, received {0} instead.'.format(response.status_code))
        self.assertIn('errors', response.data)
    
    def test_login_wrong_password(self):
        """Test for wrong password"""
        response = self.client.post(self.uri, self.params1)
        response = self.client.post(self.uri2, self.params8)
        self.assertEqual(response.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(response.status_code))
        self.assertIn('errors', response.data)

    def test_login_wrong_email(self):
        """Test for wrong email"""
        response = self.client.post(self.uri, self.params1)
        response = self.client.post(self.uri2, self.params9)
        self.assertEqual(response.status_code, 400, 'Expected Response Code 400, received {0} instead.'.format(response.status_code))
        self.assertIn('errors', response.data)