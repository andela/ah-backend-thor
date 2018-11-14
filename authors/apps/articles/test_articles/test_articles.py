from authors.apps.articles.models import Article, Rate, User
from json import loads, dumps
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

        self.login2 = {
            "user": {
                "email": "jude2jfg@fox.com",
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

        self.signUp2 = {
            "user": {
                "username": "judme29",
                "email": "jude2jfg@fox.com",
                "password": "1234qwerty"
            }
        }

        self.user_rates_signup = {
            "user": {
                "username": "jake23",
                "email": "jake@fox.com",
                "password": "1234jake"
            }
        }

        self.user_rates_login = {
            "user": {
                "email": "jake@fox.com",
                "password": "1234jake"
            }
        }

        self.rate = {
            "rate": 4
        }
        self.client = APIClient()
        self.response1 = self.client.post(
            signup_url, self.signUp, format='json')

        self.response1_user_rates = self.client.post(
            signup_url, self.user_rates_signup, format='json')

        self.response10 = self.client.post(
            signup_url, self.signUp2, format='json')

        User.objects.filter(email="jude2jg@fox.com").update(is_verified=True)
        self.response2 = self.client.post(
            login_url, self.login, format='json')
        self.token = self.response2.data['user_token']

        self.headers = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

        User.objects.filter(email="jude2jfg@fox.com").update(is_verified=True)
        self.response9 = self.client.post(
            login_url, self.login2, format='json')
        self.token = self.response9.data['user_token']
        self.headers2 = {'HTTP_AUTHORIZATION': f'Token {self.token}'}

        User.objects.filter(email="jake@fox.com").update(is_verified=True)
        self.response_user_rates = self.client.post(
            login_url, self.user_rates_login, format='json')
        self.token_user_rates = self.response_user_rates.data['user_token']
        self.headers_user_rates = {
            'HTTP_AUTHORIZATION': f'Token {self.token_user_rates}'}

        self.response4 = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        self.response3 = self.client.get(
            articles_url, format='json')
        self.response6 = self.client.get(
            f'{articles_url}{slug}', format='json') 
        self.slug = self.response4.data['slug']

    def test_user_can_get_status(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"like_status": "like"}
        num = dict(resp.data)['id']
        res = self.client.get(f"{articles_url}{num}/like_status", **self.headers, format='json')
        res2 = self.client.post(f"{articles_url}{num}/like_status", self.data,**self.headers, format='json')
        res3 = self.client.get(f"{articles_url}{num}/like_status", format='json')
        res4 = self.client.post(f"{articles_url}{num}/like_status", self.data, format='json')
        
        self.assertTrue(res.status_code == 200)
        self.assertIn('error', res.data)
        self.assertEqual(res2.status_code, 201)
        self.assertIn('like_status', loads(dumps(res3.data))[0])
        self.assertEqual(res4.status_code, 403)
        self.assertIn('detail', res4.data)

    def test_user_can_get_status_nonexistant_article(self):
        res2 = self.client.get(f"{articles_url}49/like_status", **self.headers, format='json')
        self.assertTrue(res2.status_code == 500)
        self.assertIn('error', res2.data)

    def test_article_not_yet_liked(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']
        res = self.client.get(f"{articles_url}{num}/like_status", **self.headers, format='json')
        self.assertTrue(res.status_code == 200)
        self.assertIn('error', res.data)

    def test_user_can_like_article(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"like_status": "like"}
        num = dict(resp.data)['id']
        res = self.client.post(f"{articles_url}{num}/like_status", self.data,**self.headers, format='json')

        self.assertTrue(res.status_code == 201)
        self.assertIn('like_status', res.data)

    def test_user_can_update_like_status(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"like_status": "like"}
        num = dict(resp.data)['id']
        res = self.client.put(f"{articles_url}{num}/like_status", self.data,**self.headers, format='json')

        self.assertTrue(res.status_code == 500)
        res = self.client.post(f"{articles_url}{num}/like_status", self.data,**self.headers, format='json')
        self.assertTrue(res.status_code, 201)
        self.assertIn('like_status', res.data)

    def test_wrong_user_can_update_like_status(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"like_status": "like"}
        num = dict(resp.data)['id']
        self.data2 = {"like_status": "dislike"}
        res1 = self.client.post(f"{articles_url}{num}/like_status", self.data, **self.headers, format='json')
        res = self.client.put(f"{articles_url}{num}/like_status", self.data2, **self.headers2 , format='json')
        
        self.assertTrue(res1.status_code, 201)
        self.assertTrue(res.status_code, 500)
        self.assertIn('error', res.data)
        self.assertEqual('Only judme29 can edit this!', res.data['error'])


    def test_user_can_post_article(self):
        self.assertEqual(self.response4.status_code, 201)
        self.assertIn('id', self.response4.data)
        self.assertIn('slug', self.response4.data)
        self.assertIn('body', self.response4.data)

    def test_user_can_get_article(self):
        self.assertEqual(self.response3.status_code, 200)

    def test_user_can_get_article_byId(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']

        response5 = self.client.get(
            f'{articles_url}{num}', format='json')

        self.assertEqual(response5.status_code, 200)
        self.assertTrue(isinstance(response5.data, ReturnDict))

    def test_user_post_badTitle(self):
        resp = self.client.post(
            articles_url, self.bad_title, **self.headers, format='json')
        self.assertTrue(resp.status_code, 500)
        self.assertIn('error', resp.data)

    def test_user_post_missing_fields(self):
        resp = self.client.post(
            articles_url, self.missing_fieilds, **self.headers, format='json')

        self.assertTrue(resp.status_code, 500)
        self.assertIn('error', resp.data)

    def test_user_can_get_article_bySlug(self):
        self.assertEqual(self.response6.status_code, 200)
        self.assertTrue(isinstance(self.response6.data, ReturnDict))

    def test_user_can_delete_article(self):

        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"like_status": "like"}
        num = dict(resp.data)['id']
        res = self.client.get(f"{articles_url}{num}/like_status", **self.headers, format='json')
        res2 = self.client.post(f"{articles_url}{num}/like_status", self.data,**self.headers, format='json')
        res3 = self.client.get(f"{articles_url}{num}/like_status", format='json')
        res4 = self.client.post(f"{articles_url}{num}/like_status", self.data, format='json')
        
        self.assertTrue(res.status_code == 200)
        self.assertIn('error', res.data)
        self.assertEqual(res2.status_code, 201)
        self.assertIn('like_status', loads(dumps(res3.data))[0])
        self.assertEqual(res4.status_code, 403)
        self.assertIn('detail', res4.data)

    def test_user_can_get_status_nonexistant_article(self):
        res2 = self.client.get(f"{articles_url}49/like_status", **self.headers, format='json')
        self.assertTrue(res2.status_code == 500)
        self.assertIn('error', res2.data)

    def test_article_not_yet_liked(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']
        res = self.client.get(f"{articles_url}{num}/like_status", **self.headers, format='json')
        self.assertTrue(res.status_code == 200)
        self.assertIn('error', res.data)

    def test_user_can_like_article(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"like_status": "like"}
        num = dict(resp.data)['id']
        res = self.client.post(f"{articles_url}{num}/like_status", self.data,**self.headers, format='json')

        self.assertTrue(res.status_code == 201)
        self.assertIn('like_status', res.data)
