from unicodedata import category
from rest_framework import serializers
from django.contrib.auth.models import User
#from django.contrib.auth.models import User

from .models import Comic, Categoria
#from inventories import models

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = "__all__"

class ComicSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer()
    class Meta:
        model = Comic
        fields = "__all__"

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name')
