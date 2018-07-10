from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from authors.apps.authentication.models import User
from .models import Profile
from .signals import make_profile
from mock import call, patch, MagicMock
from django.db.models.signals import post_save
from django.dispatch import receiver
from .serializers import FollowUserSerializer
from django.core.exceptions import ValidationError


class TestProfile(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/'
        self.login_url = '/api/users/login/'
        self.user_url = '/api/user/'
        self.user_profile_url = '/api/profiles/'
        self.user_profile_url2 = '/api/profiles/David'
        self.reset_password = '/api/users/password_reset/'
        self.follow_user = '/api/profiles/jake/follow'
        self.follow_non_existent_user = '/api/profiles/dude/follow'
        self.author_follows_himself = '/api/profiles/David/followers'
        self.unfollow_non_existent_user = '/api/profiles/john/unfollow'

        self.user = {
            "user": {
                "username": "David",
                "email": "david@gmail.com",
                "password": "12345678"
            }

        }

        self.user2 = {
            "user": {
                "username": "jake",
                "email": "jake@gmail.com",
                "password": "12345678@11"
            }

        }

        self.response = self.client.post(
            self.register_url, self.user, format="json")
        User.objects.filter(email="david@gmail.com").update(is_verified=True)
        self.response2 = self.client.post(
            self.login_url, self.user, format="json")
        self.token_user = self.response2.data['user_token']
        self.headers = {'HTTP_AUTHORIZATION': "Token " + f'{self.token_user}'}

        follow_response = self.client.post(
            self.register_url, self.user2, format="json")
        User.objects.filter(email="jake@gmail.com").update(is_verified=True)
        follow_response2 = self.client.post(
            self.login_url, self.user2, format="json")
        self.token_user2 = follow_response2.data['user_token']
        self.headers2 = {
            'HTTP_AUTHORIZATION': "Token " + f'{self.token_user2}'}

    def test_user_profile(self):
        """Test signals"""
        self.assertEqual(self.response.status_code, 201)

        self.assertEqual(self.response2.status_code, 200)

        res = self.client.get(self.user_url, **self.headers, format="json")
        self.assertEqual(res.status_code, 200)

        user = {
            "user": {
                "bio": "s",
                "image": "https://hhhhhassets.imgix.net/hp/snowshoe.jpg?auto=compress&w=900&h=600&fit=crop",
                "username": "jojo3"
            }
        }
        res = self.client.put(self.user_url, user, **
                              self.headers, format="json")
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.user_profile_url, **
                              self.headers, format="json")
        self.assertEqual(res.status_code, 200)

    def test_retrive_userprofile_detail(self):
        res = self.client.get(self.user_profile_url2, **
                              self.headers, format="json")
        self.assertEqual(res.status_code, 200)

    def test_send_reset(self):
        user = {
            "user": {"email": "john@gmail.com"}
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

    # tests for following users
    def test_user_following_other_users(self):
        response3 = self.client.post(
            self.follow_user, **self.headers, format='json')
        self.assertEqual('David', response3.data['following_user'])

    def test_user_following_non_existent_user(self):
        response3 = self.client.post(
            self.follow_non_existent_user, **self.headers, format='json')
        self.assertEqual('User does not exist', response3.data['error'])

    def test_list_of_authors_user_followers(self):
        self.test_user_following_other_users()
        response3 = self.client.get(
            '/api/profiles/jake/followers', format='json')
        self.assertEqual(200, response3.status_code)

    def test_list_of_authors_user_followers_non_existent(self):
        response3 = self.client.get(
            '/api/profiles/jake/followers', format='json')
        self.assertEqual(200, response3.status_code)

    def test_list_of_authors_user_is_following(self):
        self.test_user_following_other_users()
        response3 = self.client.get(
            '/api/profiles/David/following', format='json')
        self.assertIn(
            'David', response3.data['results'][0]['following_username'])

    def test_list_of_authors_user_is_following_non_existent(self):
        response3 = self.client.get(
            '/api/profiles/jake/following', format='json')
       
        self.assertEqual([], response3.data['results'])

    def test_user_unfollow_other_users(self):
        self.test_user_following_other_users()
        response3 = self.client.delete(
            '/api/profiles/jake/unfollow', **self.headers, format='json')
        self.assertEqual('David', response3.data['user'])

    def test_already_unfollowed_user(self):
        message = 'User has been unfollowed or You are unfollowing a user you were not orignally following'
        self.test_user_unfollow_other_users()
        response3 = self.client.delete(
            '/api/profiles/jake/unfollow', **self.headers, format='json')
        self.assertIn(message, response3.data['message'])

    def test_unfollow_non_existent_user(self):
        response3 = self.client.delete(
            '/api/profiles/john/unfollow', **self.headers, format='json')
        self.assertIn('User does not exist', response3.data['message'])

    def test_retieve_profile_details_non_existent_user(self):
        res = self.client.get('/api/profiles/jack', **
                              self.headers, format="json")
        self.assertEqual('User does not exist', res.data['error'])

    def test_retieve_profile_details_followed_user(self):
        self.test_user_following_other_users()
        res = self.client.get('/api/profiles/jake', **
                              self.headers, format="json")
        self.assertEqual(True, res.data['user']['following'])

    def test_retieve_profile_details_unfollowed_user(self):
        res = self.client.get('/api/profiles/jake', **
                              self.headers, format="json")
        self.assertEqual(False, res.data['user']['following'])
