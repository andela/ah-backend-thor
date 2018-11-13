from authors.apps.articles.models import Article, Rate, User
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

        self.rate= {
                    "rate":4
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
        self.headers_user_rates = {'HTTP_AUTHORIZATION': f'Token {self.token_user_rates}'}

        self.response4 = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        self.response3 = self.client.get(
            articles_url, format='json')
        self.response6 = self.client.get(
            f'{articles_url}{slug}', format='json') 

        # self.article_id = self.response4.data['id']  
        self.slug = self.response4.data['slug']

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

        num = dict(resp.data)['id']
        res = self.client.delete(
            f'{articles_url}{num}', **self.headers, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertIn('success', res.data)

    def test_user_can_update_article(self):
        data = {
            "article": {
                "title": "cows",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian goat not cow",
                "tag_list": ["cows", "training"]

            }
        }
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']

        res = self.client.patch(
            f'{articles_url}{num}', data, **self.headers, format='json')
        self.assertEqual(res.status_code, 200)

    def test_wrong_user_update_article(self):
        data = {
            "article": {
                "title": "cows",
                "description": "Ever wonder how?",
                "body": "It takes a Jacobian goat not cow",
                "tag_list": ["cows", "training"]

            }
        }
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']

        res = self.client.patch(
            f'{articles_url}{num}', data, **self.headers2, format='json')
        self.assertEqual(res.status_code, 500)
        self.assertIn('error', res.data)

    def test_wrong_user_can_delete_article(self):

        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']
        res = self.client.delete(
            f'{articles_url}{num}', **self.headers2, format='json')
        self.assertEqual(res.status_code, 500)
        self.assertIn('error', res.data)

    def test_user_can_rate_an_article(self):
        response = self.client.post(
            '/api/articles/add_rates/{}'.format(self.slug), self.rate, **self.headers_user_rates, format='json')
        self.assertIn("how_to_train_your_dragon", response.data['slug'])

    def test_author_cannot_rate_his_article(self):
        response = self.client.post(
            '/api/articles/add_rates/{}'.format(self.slug), self.rate, **self.headers, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("You can not rate your article", response.data['message'])

    def test_display_average_rating_of_an_article_not_rated(self):
        response = self.client.get('/api/articles/view_rates/{}'.format(self.slug), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, response.data['average_ratings'])

    def test_display_average_rating_of_an_article_rated(self):
        self.test_user_can_rate_an_article()
        response = self.client.get('/api/articles/view_rates/{}'.format(self.slug), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(4, response.data['average_ratings'])

