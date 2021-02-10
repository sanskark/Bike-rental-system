from django.db.models.signals import post_save
from bikerental.models import User
from django.dispatch import receiver
from .models import DealerProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
        if created and instance.is_dealer:
            DealerProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.is_dealer:
        instance.dealerprofile.save()