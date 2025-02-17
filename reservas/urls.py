from django.urls import path, include
from . import views

app_name = "reservas"

urlpatterns = [
    path("", views.reservas, name='reservas'),
    path('pesquisa_reserva/', views.pesquisa_reserva, name='pesquisa_reserva'),
    path('altera_reserva/', views.altera_reserva, name='altera_reserva'),
    path('deleta_reserva/', views.deleta_reserva, name='deleta_reserva'),
    path('fechar_reserva/', views.fechar_reserva, name='fechar_reserva'),
]
