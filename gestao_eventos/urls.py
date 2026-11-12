from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contas/', include('usuarios.urls')),
    path('', include('eventos.urls')),
]

# Em desenvolvimento, serve as imagens enviadas pelos usuários (pasta media/).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)