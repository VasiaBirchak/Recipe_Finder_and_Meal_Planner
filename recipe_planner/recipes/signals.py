from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from .utils import get_spoonacular_hash


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = UserProfile.objects.create(user=instance)
        spoonacular_hash, spoonacular_password, spoonacular_username = (
            get_spoonacular_hash(instance)
        )
        if spoonacular_hash:
            user_profile.spoonacular_hash = spoonacular_hash
            user_profile.spoonacular_password = spoonacular_password
            user_profile.spoonacular_username = spoonacular_username
            user_profile.save()
    else:
        instance.userprofile.save()
