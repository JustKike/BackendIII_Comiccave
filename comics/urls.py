from django.urls import path
from . import views
# importamos el archivo de configuracion de django
from django.conf import settings
# importamos la ruta estatica que se requiere
from django.contrib.staticfiles.urls import static
from comics.views import UserToken


urlpatterns = [

    path('',views.inicio, name='inicio'),
    path('accounts/login/',views.login,name='login'),
    path('logout/>',views.logout_view,name='logout'),
    path('register/',views.register, name='register'),
    path('accounts/login/register/',views.register, name='register'),
    path('inicio',views.inicio, name='inicio'),
    path('nosotros',views.nosotros, name='nosotros'),
    path('consultas',views.consultas, name='consultas'),
    path('historietas',views.historietas, name='historietas'),
    path('historietas/crear',views.crear, name='crear'),
    path('historietas/editar',views.editar, name='editar'),
    path('eliminar/<int:id>',views.eliminar, name='eliminar'),
    path('historietas/editar/<int:id>',views.editar, name='editar'),
    path('usuarios',views.usuarios, name='usuarios'),
    path('usuarios/crearUsuario',views.crearUsuario, name='crearUsuario'),
    path('eliminarUsuario/<int:id>',views.eliminarUsuario, name='eliminarUsuario'),
    path('usuarios/editarUsuario/<int:id>',views.editarUsuario, name='editarUsuario'),
    path('refresh-token/',UserToken.as_view, name='refresh-token'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)