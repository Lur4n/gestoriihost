from django.urls import path
from . import views

app_name = "financeiro"

urlpatterns = [
   path('', views.financeiro, name='financeiro'),
   path('produto/', views.produto, name='produto'),
   path('caixa/', views.caixa, name='caixa'),
   path('venda/', views.venda, name='venda'),
   path('estoque/', views.estoque, name='estoque'),
   path('categoria/', views.categoria, name='categoria'),
   path('criar_categoria/', views.criar_categoria, name='criar_categoria'),
   path('criar_produto/', views.criar_produto, name='criar_produto'),
   path('gerenciar_estoque/', views.criar_estoque, name='criar_estoque'),
   path('criar_venda/', views.criar_venda, name='criar_venda'),
   path('listar_vendas/', views.listar_vendas, name='listar_vendas'),

]