from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path("main", views.main, name="main"),
    path("reservas/", views.lista_reservas, name="lista_reservas"),
]
