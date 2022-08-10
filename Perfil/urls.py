from django.urls import path
from . import views
# importamos el archivo de configuracion de django
from django.conf import settings
# importamos la ruta estatica que se requiere
from django.contrib.staticfiles.urls import static


urlpatterns = [

    path('profile',views.perfil_view, name='profile'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)