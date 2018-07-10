from django.db.models.signals import post_save
from django.dispatch import receiver
from authors.apps.profiles.models import Profile
from .models import User

def save_inst(instance, id,  name="image"):
    userprofile = Profile.objects.get(profile_user_id=id)
    if name =="image":
        userprofile.image = instance.image
    elif name == "bio":
        userprofile.bio = instance.bio
    userprofile.save()

def save_profile(id, instance, instance_name):
    if str(instance_name) == "image" and instance.image:
        save_inst(instance, id, name="image")
    elif str(instance_name) == "bio" and instance.bio:
        save_inst(instance, id, name="bio")


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
