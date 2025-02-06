from django.shortcuts import render


# Create your views here.
def lista_reservas(request):
    return render(request, "lista_reservas.html")
