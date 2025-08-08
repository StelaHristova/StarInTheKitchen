from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from StarInTheKitchen.app_users.models import AppUser, Profile
from StarInTheKitchen.app_users.tasks import send_email_to_new_registered_user


@receiver(post_save, sender=Profile)
def create_profile(sender, instance, created, **kwargs):
    if created:

        # profile = Profile(
        #     user=instance
        # )
        #
        # profile.save()

        group = Group.objects.filter(name='regular_users').first()
        if group:
            instance.user.groups.add(group)

        try:
            send_email_to_new_registered_user(instance.user.email, instance.get_full_name())
            # send_email_to_new_registered_user.delay(instance.email, instance.profile.get_full_name())
        except Exception as e:
            print(f"Email sending failed: {e}")