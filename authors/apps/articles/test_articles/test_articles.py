from authors.apps.articles.models import Article
from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

User = get_user_model()
articles_url = reverse('articles:list_create_articles')
signup_url = reverse('authentication:create_user')
login_url = reverse('authentication:login')
slug = "how_to_train_your_dragon"


class ArticlesTest(APITestCase):

    def setUp(self):
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

        self.bad_title = {
            "article": {
                "title": "2",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
                "tag_list": ["dragons", "training"],
                "image_url": "https://i.stack.imgur.com/xHWG8.jpg",
                "audio_url": "https://google.com/cpw.jpg"
            }
        }

        self.missing_fieilds = {
            "article": {
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian",
            }
        }

        self.login = {
            "user": {
                "email": "jude2jg@fox.com",
                "password": "1234qwerty"
            }
        }

        self.signUp = {
            "user": {
                "username": "judme23",
                "email": "jude2jg@fox.com",
                "password": "1234qwerty"
            }
        }
        self.client = APIClient()
        self.response1 = self.client.post(
            signup_url, self.signUp, format='json')

        User.objects.filter(email="jude2jg@fox.com").update(is_active=True)
        self.response2 = self.client.post(
            login_url, self.login, format='json')
        self.token = self.response2.data['user_token']
        headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

        self.response4 = self.client.post(
            articles_url, self.article, **headers, format='json')

        self.response3 = self.client.get(
            articles_url, format='json')

        self.response5 = self.client.get(
            f'{articles_url}{[n for n in [1,2,3,4,5]][1]}', format='json')
        

        self.response6 = self.client.get(
            f'{articles_url}{slug}', format='json')


    def test_user_can_post_article(self):
        self.assertEqual(self.response4.status_code, 201)
        self.assertIn('id', self.response4.data)
        self.assertIn('slug', self.response4.data)
        self.assertIn('body', self.response4.data)

    def test_user_can_get_article(self):
        self.assertEqual(self.response3.status_code, 200)
        self.assertTrue( isinstance(self.response3.data, ReturnList))
   
    def test_user_can_get_article_byId(self):
        self.assertEqual(self.response5.status_code, 200)
        self.assertTrue( isinstance(self.response5.data, ReturnDict))

    def test_user_can_get_article_bySlug(self):
        self.assertEqual(self.response6.status_code, 200)
        self.assertTrue( isinstance(self.response6.data, ReturnDict))
