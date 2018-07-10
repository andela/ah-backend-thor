from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.apps.profiles.models import Profile
from .models import User



def save_profile(id, instance, instance_name):
    if str(instance_name) == "image":
        if instance.image:
            userprofile = Profile.objects.get(profile_user_id=id)
            userprofile.image = instance.image
            userprofile.save()
    elif str(instance_name) == "bio":
        if instance.bio:
            userprofile = Profile.objects.get(profile_user_id=id)
            userprofile.bio = instance.bio
            userprofile.save()


@receiver(post_save, sender=User)
def make_profile(sender, instance, created, **kwargs):

    if created:
        user_profile = Profile(profile_user=instance)
        user_profile.save()

    vr = instance.id
    try:
        save_profile(vr, instance, "image")
        save_profile(vr, instance, "bio")
    
    except AttributeError as e:
        return e
