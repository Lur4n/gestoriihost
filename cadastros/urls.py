from django.urls import path
from . import views

app_name = "cadastros"

urlpatterns = [

    # LIDANDO COM RESERVA
    path('criar_reserva/', views.criar_reserva, name='criar_reserva'),
   
    # LIDANDO COM QUARTO
    path('criar_quarto/', views.criar_quarto, name='criar_quarto'),
    path('apagar_quarto/', views.apagar_quarto, name='apagar_quarto'),
    path('busca_quarto_id/', views.busca_quarto_id, name='busca_quarto_id'),
    path('editar_quarto/', views.editar_quarto, name='editar_quarto'),
    
    # LIDANDO COM HOSPEDE
    path('criar_hospede/', views.criar_hospede, name='criar_hospede'),
    path('busca_hospede/', views.busca_hospede, name='busca_hospede'),
    path('busca_hospede_id/', views.busca_hospede_id, name='busca_hospede_id'),
    path('editar_hospede/', views.editar_hospede, name='editar_hospede'),
    path('apagar_hospede/', views.apagar_hospede, name='apagar_hospede'),
]
