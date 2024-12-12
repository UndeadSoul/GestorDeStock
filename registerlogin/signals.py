from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_group(sender, instance, created, **kwargs):
    if created:
        try:
            group3=Group.objects.get(name="administrador")
        except:
            group1=Group.objects.create(name="trabajadores")
            group2=Group.objects.create(name="jefes")
            group3=Group.objects.create(name="administrador")

        instance.user.groups.add(group3)