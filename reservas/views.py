from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Usuario, Reserva

# Create your views here.

def reservas(request):
    if(request.method == 'POST'):
        nome = request.POST.get('num_quarto')
        messages.error(request, nome)
        return render(request, 'index.html')
    
    reserva_lista = Reserva.objects.all().order_by("id")
    # messages.warning(request, reserva_lista)

    return render(request, 'index.html', {'reserva_lista': reserva_lista})


