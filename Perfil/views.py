from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.views import Token
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages
from django.contrib import messages
from django.contrib.sessions.models import Session
from .models import Profile
from datetime import datetime

# Create your views here.
@login_required
def perfil_view(request):
     # Guardamos la informacion del modelo
    try:
        token =  Token.objects.get(user=request.user)
        perfil = Profile.objects.filter(user = request.user.id)
        # try:
        #     perfil = Profile.objects.filter(user = request.user.id)
        # except:
        #     newProfile = Profile.insert(
        #         user = request.user.id,
        #         bio = 'Im an User',
        #         avatar = '',
        #         portada_perfil = '',
        #         departamento = 'Cliente',
        #     )
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
    return render(request, 'usuarios/profile_usuario.html',{'perfil': perfil})