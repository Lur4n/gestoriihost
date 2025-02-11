from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("autenticacao.urls")),
    path("core/", include("core.urls")),
    path("cadastros/", include("cadastros.urls")),
    # path("reservas/", include("reservas.urls")),
]
