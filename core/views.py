from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Reserva

@login_required
def main(request):
    quarto_lista = Quarto.objects.all().order_by("num_quarto")
    return render(request, "main.html", {'quarto_lista': quarto_lista})

def quartos_reservados(request):
   reservados = Quarto.objects.filter(disponibilidade=2)
   return render(request, "main.html", {'quarto_lista': reservados})

def quartos_disponiveis(request):
   disponiveis = Quarto.objects.filter(disponibilidade=1)
   return render(request, "main.html", {'quarto_lista': disponiveis})

def quartos_indisponiveis(request):
   indisponiveis = Quarto.objects.filter(disponibilidade=3)
   return render(request, "main.html", {'quarto_lista': indisponiveis})