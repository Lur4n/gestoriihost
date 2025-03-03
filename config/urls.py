from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
   path('admin/', admin.site.urls),
   path("", include("autenticacao.urls")),
   path("core/", include("core.urls")),
   path("cadastros/", include("cadastros.urls")),
   path('reservas/', include("reservas.urls")),
   path('financeiro/', include("financeiro.urls")),
   
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
