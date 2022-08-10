from os import truncate
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.shortcuts import redirect

# Create your models here.
class Base(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default="Generic")

    class Meta: abstract = True

class Categoria(Base):
    descripcion = models.CharField(max_length=64, default="Generic",verbose_name='Categoria')

    def __str__(self):
        return self.descripcion


# Consultas con el manager 
class ComicManager(models.Manager):
# 1 objtener por titulo
    def get_by_titulo(self, titulo):
        return self.filter(titulo__icontains=titulo)
# 2 objtener por descripcion
    def get_by_descripcion(self, descripcion):
        return self.filter(descripcion__icontains=descripcion)
# 3 ordenar por nombre
    def order_by_titulo(self):
        return super().get_queryset().order_by('titulo')
# 4 filtrar por fecha de creaciones
    def get_by_dateUpdated(self,date):
        return self.filter(updated_at__icontains=date)


class Comic(Base):
    id = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default="Generic", verbose_name='Categoria')
    titulo = models.CharField(max_length=100, verbose_name='Titulo')
    imagen = models.ImageField(upload_to='imagenes/',verbose_name='Imagen',null=True)
    descripcion = models.TextField(verbose_name='Descripcion',null=True)

    # utilizar consultar del manager
    objects = ComicManager()

    # creamos una fila para mostrar titulo y descripcion
    def __str__(self):
        fila = "Titulo: " + self.titulo + " - " + "Descripcion: " + Truncator(self.descripcion).words(10, truncate='...')
        return fila

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
