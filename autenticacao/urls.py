from django.urls import path, include
from django.contrib import admin
from . import views  # Certifique-se de que há uma view no app

app_name = "autenticacao"

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    # path('reservas/', include('reservas.urls')),
]
