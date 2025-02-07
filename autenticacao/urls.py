from django.urls import path, include
from . import views  # Certifique-se de que há uma view no app

app_name = "autenticacao"

urlpatterns = [
    # path("", views.login, name="login"),
    path("login/", views.login, name="login"),
]
