from django.urls import path
from . import views

app_name = "cadastros"

urlpatterns = [
    # CADASTRO DE DEPARTAMENTO
    path('criar_reserva/', views.criar_reserva, name='criar_reserva'),
    path('criar_hospede/', views.criar_hospede, name='criar_hospede'),
    path('criar_quarto/', views.criar_quarto, name='criar_quarto'),
    path('busca_hospede/', views.busca_hospede, name='busca_hospede'),
    # path('excluir_departamento/', views.excluir_departamento, name='excluir_departamento'),
    # path('pesquisar_departamento_por_nome/', views.pesquisar_departamento_por_nome, name='pesquisar_departamento_por_nome'),
    # -------------------------
]
