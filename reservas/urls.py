from django.urls import path, include
from . import views

app_name = "reservas"

urlpatterns = [
    # Lista de reservas
    path("", views.lista_reservas, name="lista_reservas"),
    # path('obter_departamento_por_id/', views.obter_departamento_por_id, name='obter_departamento_por_id'),
    # path('excluir_departamento/', views.excluir_departamento, name='excluir_departamento'),
    # path('pesquisar_departamento_por_nome/', views.pesquisar_departamento_por_nome, name='pesquisar_departamento_por_nome'),
    # -------------------------
]
