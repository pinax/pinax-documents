from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .conf import settings
from .models import UserStorage, Document


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def ensure_userstorage(sender, **kwargs):
    if kwargs["created"]:
        user = kwargs["instance"]
        UserStorage.objects.create(user=user, bytes_total=(1024 * 1024 * 50))


# Receive the pre_delete signal and delete the file associated with the model instance.
@receiver(pre_delete, sender=Document)
def document_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.file.delete(False)
