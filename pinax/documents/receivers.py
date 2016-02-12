from django.db.models.signals import post_save
from django.dispatch import receiver

from .conf import settings
from .models import UserStorage


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_userstorage(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        UserStorage.objects.create(user=user, bytes_total=(1024 * 1024 * 50))
