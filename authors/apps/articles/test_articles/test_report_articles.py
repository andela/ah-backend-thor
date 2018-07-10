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

class TestReportArticles(ArticlesTest):
    def test_user_can_get_report_status(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"reason": "I dont like this article"}
        num = dict(resp.data)['id']
        res = self.client.get(f"{articles_url}{num}/report_status", **self.headers, format='json')
        res2 = self.client.post(f"{articles_url}{num}/report_status", self.data,**self.headers, format='json')
        res3 = self.client.get(f"{articles_url}{num}/report_status", format='json')
        res4 = self.client.post(f"{articles_url}{num}/report_status", self.data, format='json')
        
        self.assertTrue(res.status_code == 200)
        self.assertIn('error', res.data)
        self.assertEqual(res2.status_code, 201)
        self.assertIn('reported', loads(dumps(res3.data))[0])
        self.assertEqual(res4.status_code, 403)
        self.assertIn('detail', res4.data)

    def test_user_can_get_report_status_nonexistant_article(self):
        res2 = self.client.get(f"{articles_url}49/report_status", **self.headers, format='json')
        
        self.assertIn('error', res2.data)

    def test_article_not_yet_reported(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')

        num = dict(resp.data)['id']
        res = self.client.get(f"{articles_url}{num}/report_status", **self.headers, format='json')
        self.assertTrue(res.status_code == 200)
        self.assertIn('error', res.data)

    def test_user_can_report_article(self):
        resp = self.client.post(
            articles_url, self.article, **self.headers, format='json')
        self.data = {"reason": "looks ugly"}
        num = dict(resp.data)['id']
        res = self.client.post(f"{articles_url}{num}/report_status", self.data,**self.headers, format='json')
        res2 = self.client.post(f"{articles_url}100/report_status", self.data,**self.headers, format='json')
        
        self.assertTrue(res.status_code == 201)
        self.assertIn('reported', res.data)
        self.assertIn('error', res2.data)