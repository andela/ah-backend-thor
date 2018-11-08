from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from authors.apps.authentication.models import User
from .models import Profile
from .signals import make_profile
from mock import call, patch, MagicMock
from django.db.models.signals import post_save
from django.dispatch import receiver

class TestProfile(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/'
        self.login_url = '/api/users/login/'
        self.user_url = '/api/user/'
        self.user_profile_url = '/api/profiles/'
        self.user_profile_url2 = '/api/profiles/David'
        self.reset_password = '/api/users/password_reset/'

        self.user={
            "user":{
                    "username":"David",
                    "email":"david@gmail.com",
                    "password":"12345678"
                }
            }

    def test_user_profile(self):
        """Test signals"""
        response = self.client.post(self.register_url, self.user, format="json")
        self.assertEqual(response.status_code, 201)

        User.objects.filter(email="david@gmail.com").update(is_active=True)
        response = self.client.post(self.login_url, self.user, format="json")
        self.assertEqual(response.status_code, 200)

        token = response.data['user_token']
        headers = {'HTTP_AUTHORIZATION': "Token " + f'{token}'}
        res = self.client.get(self.user_url, **headers, format="jason")
        self.assertEqual(res.status_code, 200)

        user = {
            "user": {
                "bio": "s",
                "image": "https://hhhhhassets.imgix.net/hp/snowshoe.jpg?auto=compress&w=900&h=600&fit=crop",
                "username":"jojo3"
            }
        }
        res = self.client.put(self.user_url, user, **headers, format="json")
        self.assertEqual(res.status_code, 200)
       
        res = self.client.get(self.user_profile_url, **headers, format="json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.user_profile_url2, **headers, format="json")
        self.assertEqual(res.status_code, 200)
    
    def test_send_reset(self):
        user = {
            "user":{"email":"david@gmail.com"}
        }
        res = self.client.post(self.reset_password, user, format="json")
        self.assertEqual(res.status_code, 400)
    
    def test_signal(self):

        with patch('authors.apps.profiles.models.Profile.save') as mock_make_profile:
            make_profile(sender=User, instance=User(), created=True)
            self.assertEqual(mock_make_profile.call_count, 1)
    @patch("django.db.models.signals.ModelSignal.send")
    def test_signal2(self, mocker_signal):
        user = User()
        self.assertEqual(mocker_signal.call_count, 2)
