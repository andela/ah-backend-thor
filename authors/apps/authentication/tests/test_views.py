from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class TestPoll(APITestCase):
    """Test suite for the api views."""

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

        self.invalid_user = {
            "user": {
                "username": "dude",
                "email": "dude1gmail.com",
                "password": "passwor"
            }
        }

        self.valid_email = {"user":{"email":"dude1@gmail.com"}}
        self.invalid_email = {"user":{"email":""}}

    def test_register_a_new_user(self):
        """test create new user when registering"""
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])

    def test_login_un_registered_user(self):
        '''Test logging in an unregistered user '''
        response = self.client.post(self.login_url, self.user, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('A user with this email and password was not found',
                      response.data['errors']['error'][0])

    def test_user_login(self):
        '''Test registering a User and logging them in '''
        response = self.client.post(
            self.register_url, self.user, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User successfully Registered', response.data['message'])
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

    def test_reset_password(self):
        self.client.post('/api/users/', self.user, format = 'json')
        response = self.client.post('/api/users/password_reset/', self.valid_email, format='json')
        self.assertEqual(response.status_code, 201)

    def test_reset_password_missing_email(self):
        self.client.post('/api/users/', self.user, format = 'json')
        response = self.client.post('/api/users/password_reset/', self.invalid_email, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_change_password_missing_password(self):
        self.invalid_password = {"new_password":""}
        self.client.post('/api/users/', self.user, format = 'json')
        self.res = self.client.post('/api/users/password_reset/', self.valid_email, format='json')
        self.result = self.res.data['token']
        response= self.client.put('/api/users/update_password/{}'.format(self.result), self.invalid_password, format='json')
        self.assertEqual(response.status_code, 400)

    def test_change_password(self):
        self.valid_password = {"new_password":"newpassword"}
        self.client.post('/api/users/', self.user, format = 'json')
        self.res = self.client.post('/api/users/password_reset/', self.valid_email, format='json')
        self.result = self.res.data['token'] 
        response= self.client.put('/api/users/update_password/{}'.format(self.result), self.valid_password, format='json')
        self.assertEqual(response.status_code, 201)
