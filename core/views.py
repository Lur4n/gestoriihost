from django.shortcuts import render


# Create your views here.
def main(request):
    return render(request, "main.html")

def lista_reservas(request):
    return render(request, "lista_reservas.html")
