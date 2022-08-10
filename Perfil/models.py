from django.db import models
from django.contrib.auth.models import User

# Create your models here.

deparment_choices = (
    ('AC', 'Atencion_al_Cliente'),
    ('Inv', 'Inventarios'),
    ('Ven', 'Ventas'),
    ('Ad', 'Admin'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='user')
    bio = models.CharField(max_length=256, default="Im an User",verbose_name='bio')
    avatar = models.ImageField(upload_to="imagenes/avatars",verbose_name='avatar',null=True)
    portada_perfil = models.ImageField(upload_to="imagenes/portada",verbose_name='portada',null=True)
    departamento = models.CharField(max_length=32, choices=deparment_choices,verbose_name='department')

    def __str__(self):
        fila = "Usuario: " + self.user.first_name + " - " + "departamento: " + self.departamento
        return fila