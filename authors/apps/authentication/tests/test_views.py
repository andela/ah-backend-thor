from rest_framework.test import APIClient, APITestCase
from ..models import User
import os


class TestPoll(APITestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""

        self.client = APIClient()
        self.register_url = '/api/users/'
        self.login_url = '/api/users/login/'
        self.get_user_url = '/api/user/'
        self.social_authentication = '/api/rest-auth/facebook/'
        self.token = {
            "access_token": os.getenv("FB_RESPONSE_TOKEN")}
        self.atoken = {
            "access_token": os.getenv("FB_ACCESS_TOKEN")
        }

        self.user = {
            "user": {
                "username": "dude",
                "email": "dude1@gmail.com",
                "password": "password"
            }
        }

        self.invalid_user = {
            "user": {
                "username": "dude",
                "email": "dude1gmail.com",
                "password": "passwor"
            }
        }

        self.send_password_reset_email = '/api/users/password_reset/'

        self.valid_email = {
            "user": {
                "email": "dude1@gmail.com"
            }
        }

        self.empty_email = {
            "user": {
                "email": ""
            }
        }

        self.send_password_reset_email = '/api/users/password_reset/'
        self.email_link = '/api/users/update_password/{}'

    def test_user_token_details(self):
        response = self.client.post(
            self.social_authentication, self.token, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Invalid data'}
        )
    def test_user_token_detail(self):
        response = self.client.post(
            self.social_authentication, self.atoken, format='json')
        self.assertEqual(response.status_code, 201)
        response2 = self.client.post(
            self.social_authentication, self.atoken, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_register_a_new_user(self):
        """test create new user when registering"""
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])

    def test_login_un_registered_user(self):
        '''Test logging in an unregistered user '''
        response = self.client.post(self.login_url, self.user, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('A user with this email or password was not found !',
                      response.data['errors'])

    def test_user_login(self):
        '''Test registering a User and logging them in '''
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])
        User.objects.filter(email="dude1@gmail.com").update(is_verified=True)
        response = self.client.post(self.login_url, self.user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User successfully confirmed',
                      response.data['user_message'])

    def test_registering_an_invalid_user(self):
        '''Test registering an invalid user with wrong details '''
        response = self.client.post(
            self.register_url, self.invalid_user, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter a valid email address',
                      response.data['errors']['email'][0])

    def test_a_user_that_already_exits(self):
        ''' Tests registering a user that already exists '''
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('user with this email already exists',
                      response.data['errors']['email'][0])

    def test_get_a_user_after_register(self):
        ''' Gets a registered user '''
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])
        User.objects.filter(email="dude1@gmail.com").update(is_verified=True)
        response = self.client.post(self.login_url, self.user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User successfully confirmed',
                      response.data['user_message'])
        token = response.data['user_token']
        # self.assertIn('asasdas',token)
        headers = {'HTTP_AUTHORIZATION': "Token " + f'{token}'}
        rev = self.client.get(self.get_user_url, **headers, format='json')
        self.assertEqual(rev.status_code, 200)
        self.assertIn(
            'dude1@gmail.com', rev.data['email'])

    def test_update_a_registered_user_after_register(self):
        ''' Gets a registered user '''
        new_user = {
            "user": {
                "email": "chuckyz@gmail.com",
                "username": "chuckyz"
            }
        }
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])
        User.objects.filter(email="dude1@gmail.com").update(is_verified=True)
        response = self.client.post(self.login_url, self.user, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User successfully confirmed',
                      response.data['user_message'])
        token = response.data['user_token']
        # self.assertIn('asasdas',token)
        headers = {'HTTP_AUTHORIZATION': "Token " + f'{token}'}
        rev = self.client.put(self.get_user_url, new_user,
                              **headers, format='json')
        self.assertEqual(rev.status_code, 200)

    def test_send_password_reset_email_valid_email(self):
        self.test_register_a_new_user()
        response = self.client.post(
            self.send_password_reset_email, self.valid_email, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Check your email for the password reset link',
                      response.data['message'])

    def test_send_password_reset_email_missing_email(self):
        self.test_register_a_new_user()
        response = self.client.post(
            self.send_password_reset_email, self.empty_email, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please fill in your email', response.data['message'])

    def test_change_password_missing_password(self):
        self.empty_password = {"new_password": ""}
        self.test_register_a_new_user()
        self.res = self.client.post(
            self.send_password_reset_email, self.valid_email, format='json')
        self.token = self.res.data['token']
        response = self.client.put(self.email_link.format(
            self.token), self.empty_password, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please fill in your password', response.data['message'])

    def test_change_password_valid_password(self):
        self.valid_password = {"new_password": "newpassword"}
        self.test_register_a_new_user()
        self.res = self.client.post(
            self.send_password_reset_email, self.valid_email, format='json')
        self.token = self.res.data['token']
        response = self.client.put(self.email_link.format(
            self.token), self.valid_password, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Password updated', response.data['message'])
