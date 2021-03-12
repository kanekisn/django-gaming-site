from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Profile
from articles.models import *

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_migrate)
def groups_init(sender, **kwargs):
    articles_ct = ContentType.objects.get_for_model(Articles)

    approve = Permission.objects.get_or_create(
        codename='can_approve',
        name='Can approve articles',
        content_type=articles_ct
    )

    perms = Permission.objects.filter(
        codename__in=('add_articles', 'change_articles', 'delete_articles', 'can_approve'),
        content_type=articles_ct
    )

    mod, created = Group.objects.get_or_create(
        name = 'Moderator'
    )

    sv, created = Group.objects.get_or_create(
        name = 'Supervisor'
    )

    mod.permissions.set([perms[0], perms[1], perms[2]])
    sv.permissions.set(perms)
    