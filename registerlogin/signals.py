from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save, sender=Profile)
def add_user_to_worker_group(sender, instance, created, **kwargs):
    if created:
        try:
            worker=Group.objects.get(name="trabajador")
        except:
            worker=Group.objects.create(name="trabajador")
            worker=Group.objects.create(name="jefedebodega")
            worker=Group.objects.create(name="administrador")

        instance.user.groups.add(worker)