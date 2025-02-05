from django.urls import path, include
from . import views  # Certifique-se de que há uma view no app

app_name = 'quartos'

urlpatterns = [
        path('', views.login, name='login'),
        path('mostruario/', views.mostruario, name='mostruario'),
]
