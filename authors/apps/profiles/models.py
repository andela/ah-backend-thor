from django.db import models
from authors.apps.authentication.models import User


class Profile(models.Model):
    """Model for creating User profile"""

    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, default="")
    image = models.URLField(max_length=100, default="")
    following = models.BooleanField(default = False)
    updated_at = models.DateTimeField(auto_now=True)

class FollowUser(models.Model):
    following_username = models.CharField(max_length = 255)
    followed_username = models.CharField(max_length = 255)
    
    
