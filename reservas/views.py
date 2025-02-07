from django.shortcuts import render, redirect


# Create your views here.
def lista_reservas(request):
    return render(request, "lista_reservas.html")

def login(request):
    return render(request, "login.html")