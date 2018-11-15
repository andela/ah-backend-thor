from rest_framework.test import APIClient, APITestCase
from authors.apps.authentication.models import User
from authors.apps.articles.models import Article
from rest_framework import status

signup_url = "/api/users/"
login_url = "/api/users/login/"
articles_url = "/api/articles/"
email_url = '/api/articles/how_to_train_your_dragon/email'
twitter_url = '/api/articles/how_to_train_your_dragon/twitter'
facebook_url = '/api/articles/how_to_train_your_dragon/facebook'


class TestShareArticles(APITestCase):

    def setUp(self):

        self.client = APIClient()
        self.signUp = {
            "user": {
                "username": "jake",
                "email": "jake@fox.com",
                "password": "1234qwerty"
            }
        }

        self.login = {
            "user": {
                "email": "jake@fox.com",
                "password": "1234qwerty"
            }
        }

        self.client = APIClient()
        self.response1 = self.client.post(
            signup_url, self.signUp, format='json')

        User.objects.filter(email="jake@fox.com").update(is_verified=True)
        self.response2 = self.client.post(
            login_url, self.login, format='json')
        self.token = self.response2.data['user_token']
        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

        self.article = {
            "article": {
                "title": "How to train your dragon",
                "description": "EEver wonder how?",
                "body": "How long can I take to be a good programmer",
                "tag_list": ["coding", "python"],
                "image_url": "https://i.stack.imgur.com/xHWG8.jpg",
                "audio_url": "https://google.com/cpw.jpg",
            }
        }

        self.client.post(
            articles_url, self.article, **self.headers, format="json"
        )

    def test_share_via_email(self):
        response = self.client.post(
            email_url, **self.headers, format='json')
        self.assertIn("Check your email for the link to article",
                      response.data['message'])

    def test_share_via_twitter(self):
        response = self.client.post(
            twitter_url, **self.headers, format='json')
        self.assertIn("Twitter link",
                      response.data['message'])

    def test_share_via_facebook(self):
        response = self.client.post(
            facebook_url, **self.headers, format='json')
        self.assertIn("Facebook link",
                      response.data['message'])

    def test_share_via_facebook_wrong_article(self):
        response = self.client.post(
            '/api/articles/how_/facebook', **self.headers, format='json')
        self.assertIn("Article not found",
                      response.data['message'])

    def test_share_via_twitter_wrong_article(self):
        response = self.client.post(
            '/api/articles/how_/twitter', **self.headers, format='json')
        self.assertIn("Article not found",
                      response.data['message'])

    def test_share_via_email_wrong_article(self):
        response = self.client.post(
            '/api/articles/how_/email', **self.headers, format='json')
        self.assertIn("Article not found",
                      response.data['message'])
