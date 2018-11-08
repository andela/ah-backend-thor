from django.db import models
from authors.apps.articles.models import Article
from authors.apps.authentication.models import User


class Comments(models.Model):
    body = models.TextField()
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(
        Article, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Comments object {}'.format(self.body)
