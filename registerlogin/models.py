from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

class Profile(models.Model):

    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile",verbose_name="Usuario")
    image=models.ImageField(default="usuario_defecto.jpg",verbose_name="Imagen de perfil")
    rut=models.CharField(max_length=12,null=True,blank=True,verbose_name="Rut")
    name=models.CharField(max_length=50,null=True,blank=True,verbose_name="Nombre")
    email=models.EmailField(max_length=254, verbose_name="Correo")
    telephone=models.CharField(max_length=150,null=True,blank=True,verbose_name="Telefono")

    class Meta:
        verbose_name="perfil"
        verbose_name_plural="perfiles"
        ordering=["-id"]

    def __str__(self):
        return self.user.username
    
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender,instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)