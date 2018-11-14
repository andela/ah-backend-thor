from json import dumps, loads

from django.contrib.auth import get_user_model
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from authors.apps.articles.models import Article, Rate, User
from .test_articles import ArticlesTest

User = get_user_model()
articles_url = reverse('articles:list_create_articles')
signup_url = reverse('authentication:create_user')
login_url = reverse('authentication:login')
slug = "how_to_train_your_dragon"

class TestArticles(ArticlesTest):
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
            f'{articles_url}{num}', **self.headers, format='json')
        
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
