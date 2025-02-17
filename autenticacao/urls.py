from django.urls import path
from django.contrib import admin
from . import views  # Certifique-se de que há uma view no app

app_name = "autenticacao"

urlpatterns = [
   path('admin/', admin.site.urls),
   path("", views.login, name="login"),
   path("get_perfis/", views.get_perfis, name="get_perfis"),
   path("logout/", views.logout, name="logout"),
   path("esqueci_senha/", views.esqueci_senha, name="esqueci_senha"),
   path("recuperar_senha/", views.recuperar_senha, name="recuperar_senha"),
   path('recuperar_senha/<str:token>/', views.recuperar_senha, name='recuperar_senha'),
   path("editar_perfil/", views.editar_perfil, name="editar_perfil"),
]
