from django.urls import path, include

urlpatterns = [
    path('', include('autenticacao.urls')),
    path('nossos_quartos/', include('quartos.urls')),
    # path("admin/", admin.site.urls),
]
