from authors.apps.authentication.models import User
from django.db import models
from taggit.managers import TaggableManager

class Article(models.Model):
    slug = models.CharField(max_length=100, blank=False)
    title = models.CharField(max_length=300, blank=False)
    description = models.TextField(blank=False)
    body = models.TextField(blank=False)
    tag_list = TaggableManager(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorited = models.BooleanField(default=False)
    favorites_count = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField(blank=False)
    audio_url = models.URLField(blank=True, null=True)
    read_time = models.CharField(max_length=100, blank=False)
    fav_user = models.ManyToManyField(User, related_name='fav_users')

    def __str__(self):
        return f"{self.title}, {self.body}"


class Rate(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='article_id')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_who_rated_article')
    rate = models.IntegerField(default=0)

    def __repr__(self):
        return self.rate

class LikeArticle(models.Model):
    like = 'like'
    dislike = 'dislike'
    choices = ((like, 'like'), (dislike, 'dislike'))
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    like_status = models.CharField(max_length=9, choices=choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.like_status
