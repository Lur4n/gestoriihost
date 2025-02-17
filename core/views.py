from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Reserva

# Create your views here.

@login_required
def main(request):
    quarto_lista = Quarto.objects.all().order_by("num_quarto")
    return render(request, "main.html", {'quarto_lista': quarto_lista})

