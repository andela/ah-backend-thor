from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.apps.profiles.models import Profile
from .models import User

@receiver(post_save, sender=User)
def make_profile(sender, instance, created, **kwargs):
    
    if created:
        user_profile = Profile(profile_user=instance)
        user_profile.save()
    try:
        if instance.image is not None:
            yyy = instance.id
            userprofile = Profile.objects.get(profile_user_id=yyy) 
            userprofile.image = instance.image 
            userprofile.save()

        if instance.bio is not None:
            yyy = instance.id
            userprofile = Profile.objects.get(profile_user_id=yyy) 
            userprofile.bio = instance.bio 
            userprofile.save()
        
    except AttributeError as e:
        return e
