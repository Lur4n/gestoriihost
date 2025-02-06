from django.urls import path, include
from . import views  # Certifique-se de que há uma view no app

urlpatterns = [
        path('', views.login, name='login'),
        path('nossos_quartos/', include('quartos.urls')),
]
