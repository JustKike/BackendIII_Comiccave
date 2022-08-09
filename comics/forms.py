# requerimos formulario
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# para generar un formulario apartir del modelo
from .models import Comic, Categoria


# Creamos una clase para modelar
class ComicForm(forms.ModelForm):
    class Meta:
        model = Comic
        fields = '__all__'

class CateForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
        help_texts = {k:"" for k in fields }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        help_texts = {k:"" for k in fields }