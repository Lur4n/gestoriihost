from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
   path("main", views.main, name="main"),
   path("quartos_reservados/", views.quartos_reservados, name="quartos_reservados"),
   path("quartos_disponiveis/", views.quartos_disponiveis, name="quartos_disponiveis"),
   path("quartos_indisponiveis/", views.quartos_indisponiveis, name="quartos_indisponiveis"),
] 
