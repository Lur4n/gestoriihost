from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def reservas(request):
    return render(request, 'index.html')

def lista_reservas(request):
    return redirect('reservas:lista_reservas')
    # return render(request, "lista_reservas.html")
