from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()


@receiver(user_logged_in)
def set_user_online(sender, user, request, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.status = 'online'
    profile.save()

@receiver(user_logged_out)
def set_user_offline(sender, user, request, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.status = 'offline'
    profile.save()
