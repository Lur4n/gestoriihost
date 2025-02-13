from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Usuario, Reserva

# Create your views here.

def reservas(request):
   # Pegando 1 quarto
   if request.method == 'POST':
    num_quarto = request.POST.get('num_quarto')
    reserva_unica = Reserva.objects.filter(num_quarto=num_quarto).order_by("-id")
    
    if reserva_unica.exists():
        # Caso exista uma reserva, mostra a mensagem de erro
        messages.error(request, f"Reserva já existente para o quarto {num_quarto}.")
    else:
        # Caso não exista uma reserva, pode criar uma nova ou outra ação
        messages.success(request, f"Quarto {num_quarto} disponível para nova reserva.")

    return render(request, 'index.html', {'reserva_lista': reserva_unica})


   # Pegando todos os quartos
   reserva_lista = Reserva.objects.all().order_by("-is_active", "num_quarto")
   # reserva_lista.order_by("num_quarto")
   # messages.warning(request, reserva_lista)

   return render(request, 'index.html', {'reserva_lista': reserva_lista})


