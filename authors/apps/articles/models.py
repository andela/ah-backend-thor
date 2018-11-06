from authors.apps.authentication.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Article(models.Model):
    slug = models.CharField(max_length=100, blank=False)
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(blank=False)
    body = models.TextField(blank=False)
    tag_list = ArrayField(models.CharField(max_length=200), blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited = models.BooleanField(default=False)
    favorites_count = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    audio_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title, self.body


class Rate(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name= 'article_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'user_who_rated_article')
    rate = models.IntegerField(default=0)

    def __repr__(self):
        return self.rate

