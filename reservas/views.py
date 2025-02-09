from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required
def lista_reservas(request):
    return redirect('reservas:lista_reservas')
    # return render(request, "lista_reservas.html")
