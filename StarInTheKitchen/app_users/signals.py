from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from StarInTheKitchen.app_users.models import AppUser, Profile


@receiver(post_save, sender=AppUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            user=instance
        )

        profile.save()

        group = Group.objects.filter(name='regular_users').first()
        instance.group.add(group)