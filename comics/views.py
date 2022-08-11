from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.views import Token

from comics import authentication
from .serializers import UserTokenSerializer
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import Comic, Categoria
from Perfil.models import Profile
from .forms import ComicForm,UserForm
from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from django.views import View
from comics.authentication_mixins import Autentication
from .mixins import LoginYSuperUsuarioMixin

class UserToken(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        try:
            user_token = Token.objects.get(
                user = UserTokenSerializer().Meta.model.objects.filter(username = username).first()
                )
            messages.info(request,{'token': user_token.key})
        except:
            messages.error(request,{'error': 'Credenciales incorrectas'})


""" Inicia gestion de Login/logout """
# Iniciar sesion
def login(request):
    if request.user.is_authenticated:
            return redirect('inicio')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_active:
                    token,created = Token.objects.get_or_create(user = user)
                    user_serializer = UserTokenSerializer(user)
                    if created:
                        messages.info(request,{
                            'token': token.key, 
                            'user': user_serializer.data,
                            },'Inicio de sesion exitoso.')
                    else:
                        # manejo de sesiones
                        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                        if all_sessions.exists():
                            for session in all_sessions:
                                session_data = session.get_decoded()
                                if str(user.id) == session_data.get('_auth_user_id'):
                                    session.delete()
                        token.delete()
                        token = Token.objects.create(user = user)
                        messages.info(request,{
                            'token': token.key, 
                            'user': user_serializer.data,
                            },'Inicio de sesion exitoso.')
                else:
                    messages.info(request, 'Este usuario no puede iniciar sesion.')
                
                return redirect('inicio')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            
        return render(request, 'paginas/login.html')

# Cerrar sesion
@login_required
def logout_view(request):
    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
    if all_sessions.exists():
        for session in all_sessions:
            session_data = session.get_decoded()
            if str(request.user.id) == session_data.get('_auth_user_id'):
                session.delete()
                request.user.auth_token.delete()
    # logout(request)
    return redirect('login')
    
# Registro de usuarios
def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado',extra_tags='tag1 tag2')
            return redirect('inicio')
    else:
        form = UserRegisterForm()
    context = { 'form': form }
    return render(request, 'paginas/register.html', context)

""" Termina gestion de Login/logout """
    
""" Inicia gestion de usuarios """
#Gestion de usuarios
@login_required
def usuarios(request):
    try:
        token =  Token.objects.get(user=request.user)
        if request.user.is_staff:
            # Guardamos la informacion del modelo
            usuarios = User.objects.filter(is_superuser=False,is_active = True)
            # enviamos los datos a la vista mediante la variable historietas
            return render(request, 'usuarios/listar_usuario.html', {'usuarios': usuarios})
        else:
            messages.error(request,{'GESTION DE USUARIOS': 'NO TIENES PERMISO PARA ACCEDER'})
            return redirect('inicio')
    except:
        # manejo de sesiones
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if str(request.user.id) == session_data.get('_auth_user_id'):
                    session.delete()
            messages.error(request,{'error': 'NO EXISTE EL TOKEN'})
        return redirect('login')

# Agregar o crear un usuario
@login_required
def crearUsuario(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado',extra_tags='tag1 tag2')
            return redirect('usuarios')
    else:
        form = UserRegisterForm()
    context = { 'form': form }
    return render(request, 'usuarios/crear_usuario.html',context)

# eliminar un usuario
@login_required
def eliminarUsuario(request, id):
    permiso = request.user.get_all_permissions()
    print(permiso)
    if 'auth.delete_user' in permiso:
        usuario = User.objects.get(id=id)
        usuario.delete()
        messages.error(request,{'USUARIO BORRADO'})
        return redirect('usuarios')
    else:
        messages.error(request,{'error': 'NO TIENES PERMISO PARA ELIMINAR USUARIOS'})
        return redirect('usuarios')

# Editar Usuario
@login_required
def editarUsuario(request, id):
    # consulta del comic
    usuario1 = User.objects.get(id=id)
    # la pasamos al formulario
    formulario = UserForm(request.POST or None, request.FILES or None, instance=usuario1)
    # si hay un envio de informacion
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('usuarios')
    return render(request, 'usuarios/editar_usuario.html', {'formulario': formulario})

""" Termina gestion de usuarios """

""" Inicia gestion de Historietas """
# Acceder al index de historietas
@login_required
def historietas(request):
    try:
        token =  Token.objects.get(user=request.user)
        if request.user.is_staff:
            # Guardamos la informacion del modelo
            historietas = Comic.objects.all()
            # enviamos los datos a la vista mediante la variable historietas
            return render(request, 'historietas/index.html', {'historietas': historietas})
        else:
            messages.error(request,{'GESTION DE HISTORIETAS': 'NO TIENES PERMISO PARA ACCEDER'})
            return redirect('inicio')
    except:
        # manejo de sesiones
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if str(request.user.id) == session_data.get('_auth_user_id'):
                    session.delete()
            messages.error(request,{'error': 'NO EXISTE EL TOKEN'})
        return redirect('login')

# Agregar o crear un comic
@login_required
def crear(request):
    # guardamos la info del modelo
    formulario = ComicForm(request.POST or None, request.FILES or None)
    categorias = Categoria.objects.all()
    # si el formulario es valido guardar y redireccionar
    if formulario.is_valid():
        formulario.save()
        return redirect('historietas')
    return render(request, 'historietas/crear.html', {'formulario': formulario,'categorias': categorias})

# Editar un comic
@login_required
def editar(request, id):
    # consulta del comic
    comic = Comic.objects.get(id=id)
    categorias = Categoria.objects.all()
    # la pasamos al formulario
    formulario = ComicForm(request.POST or None, request.FILES or None, instance=comic)
    # si hay un envio de informacion
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('historietas')
    return render(request, 'historietas/editar.html', {'formulario': formulario,'categorias': categorias})

# eliminar un comic
@login_required
def eliminar(request, id):
    comic = Comic.objects.get(id=id)
    comic.delete()
    return redirect('historietas')

""" Termina gestion de Historietas """

# Pagina de inicio
@login_required
def inicio(request):
    # Guardamos la informacion del modelo
    historietas = Comic.objects.all()
    try:
        token =  Token.objects.get(user=request.user)
    except:
        # manejo de sesiones
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if str(request.user.id) == session_data.get('_auth_user_id'):
                    session.delete()
            messages.error(request,{'error': 'NO EXISTE EL TOKEN'})
        return redirect('login')
    return render(request, 'paginas/inicio.html', {'historietas': historietas})

# Acceder a la pagina nosotros
@login_required
def nosotros(request):
    try:
        token =  Token.objects.get(user=request.user)
    except:
        # manejo de sesiones
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if str(request.user.id) == session_data.get('_auth_user_id'):
                    session.delete()
            messages.error(request,{'error': 'NO EXISTE EL TOKEN'})
        return redirect('login')
    return render(request, 'paginas/nosotros.html')

# Acceder a la pagina consultas
@login_required
def consultas(request):
    opcion = Autentication()
    # token = request.user.auth_token.exists()
    queryset = request.GET.get('Buscar')
    querysetDate = request.GET.get('Filtrar')
    queryCateg = request.GET.get('Category')
    historietas = Comic.objects.order_by_titulo().all()
    usuarios = User.objects.all()
    categorias = Categoria.objects.all()
    try:
        token =  Token.objects.get(user=request.user)
        if request.user.is_staff:
            if queryset:
                historietas = (Comic.objects.get_by_titulo(queryset) |
                Comic.objects.get_by_descripcion(queryset)).distinct()
            else:
                if querysetDate:
                    datos = Comic.objects.get(id=querysetDate)
                    date = datos.updated_at
                    historietas = Comic.objects.get_by_dateUpdated(date)
                else:
                    if queryCateg:
                        historietas = Comic.objects.filter(categoria_id=queryCateg)
            return render(request, 'paginas/consultas.html',
        {
            'historietas': historietas,
            'usuarios': usuarios,
            'categorias': categorias,
            'opcion': opcion
        })
        else:
            messages.error(request,{'SECCION DE CONSULTAS': 'NO TIENES PERMISO PARA ACCEDER'})
            return redirect('inicio')

    except:
        # manejo de sesiones
        all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
        if all_sessions.exists():
            for session in all_sessions:
                session_data = session.get_decoded()
                if str(request.user.id) == session_data.get('_auth_user_id'):
                    session.delete()
            messages.error(request,{'error': 'NO EXISTE EL TOKEN'})
        return redirect('login')

