from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils.text import slugify

from .models import MyUser


# example of signal
@receiver(post_save, sender=MyUser, dispatch_uid='create_slug')
def create_slug(sender, **kwargs):
    user = kwargs.get('instance')  # get Model object

    if not user.slug:
        user.slug = slugify(user.get_full_name()) + "-" + str(user.pk)
        user.save()
