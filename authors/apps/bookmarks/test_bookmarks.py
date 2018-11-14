from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from authors.apps.authentication.models import User
from rest_framework.reverse import reverse


class TestProfile(APITestCase):
    def setUp(self):
        self.register_url = '/api/users/'
        self.login_url = '/api/users/login/'
        self.get_bookmark = '/api/bookmarks'
        self.post_bookmark = '/api/bookmarks/how_to_train_your_dragon'
        self.post_bookmark2 = '/api/bookmarks/how_to_train_your_dragon_'
        self.delete_bookmark = '/api/bookmarks/how_to_train_your_dragon/delete'
        self.delete_bookmark2 = '/api/bookmarks/how_to_train_your_dragon_/delete'
        self.articles_url = '/api/articles/'

        self.user = {
            "user": {
                "username": "David",
                "email": "david@gmail.com",
                "password": "12345678"
            }
        }
        self.article = {
            "article": {
                "title": "How to train your dragon",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tag_list": ["dragons", "training"],
                "image_url": "https://i.stack.imgur.com/xHWG8.jpg",
                "audio_url": "https://google.com/cpw.jpg"
            }
        }

    def test_user_profile(self):
        """Test signals"""
        response = self.client.post(
            self.register_url, self.user, format="json")
        self.assertEqual(response.status_code, 201)

        User.objects.filter(email="david@gmail.com").update(is_verified=True)
        response = self.client.post(self.login_url, self.user, format="json")
        self.assertEqual(response.status_code, 200)

        token = response.data['user_token']
        headers = {'HTTP_AUTHORIZATION': "Token " + f'{token}'}
        self.response = self.client.post(
            self.articles_url, self.article, **headers, format='json')
        self.assertEqual(self.response.status_code, 201)
        response = self.client.post(
            self.post_bookmark, **headers, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.post(
            self.post_bookmark2, **headers, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)

        response = self.client.get(self.get_bookmark,
                                   **headers, format="json")
        self.assertEqual(response.status_code, 200)

        response = self.client.delete(self.delete_bookmark,
                                      **headers, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(
            self.delete_bookmark2, **headers, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('article bookmark message', response.data)

        response = self.client.get(self.get_bookmark,
                                   **headers, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)
