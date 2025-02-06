from django.urls import path, include

urlpatterns = [
    path('', include('autenticacao.urls')),
    # path("admin/", admin.site.urls),
]
