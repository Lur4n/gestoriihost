from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Usuario, Reserva, Hospede
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date

# Create your views here.

def reservas(request):
   # Pegando 1 quarto
   if request.method == 'POST':
      num_quarto = request.POST.get('num_quarto')
      reserva_unica = Reserva.objects.filter(num_quarto=num_quarto).order_by("-id")
      
      if reserva_unica.exists():
         # Caso exista uma reserva, mostra a mensagem de erro
         messages.error(request, f"Reserva já existente para o quarto {num_quarto}.")
         return render(request, 'reservas.html', {'reserva_lista': reserva_unica})
      else:
         # Caso não exista uma reserva, pode criar uma nova ou outra ação
         messages.success(request, f"Quarto {num_quarto} disponível para nova reserva.")



   # Pegando todos os quartos
   reserva_lista = Reserva.objects.all().order_by("-is_active", "-id")
   # reserva_lista.order_by("num_quarto")
   print(reserva_lista[1].check_in)
   # messages.warning(request, reserva_lista)

   return render(request, 'reservas.html', {'reserva_lista': reserva_lista})



def pesquisa_reserva(request):
   hospede_nome = request.GET.get('reserva_nome', '')
   hospede_quarto = request.GET.get('reserva_quarto', '')

   if hospede_nome:
      hospedes = Reserva.objects.filter(id_hospede__nome__icontains=hospede_nome)[:10]
      print('Passou aq com: ', hospede_nome)
      for hospede in hospedes:
         print(hospede)
         
   elif hospede_quarto:
      hospedes = Reserva.objects.filter(num_quarto__num_quarto__icontains=hospede_quarto).order_by('num_quarto')
      print('Passou aq com: ', hospede_nome)
      for hospede in hospedes:
         print(hospede)

   else:
      hospedes = Reserva.objects.all().order_by("-is_active", "num_quarto")
      print("vazio")

   return JsonResponse({
      'html': render_to_string('editar_reserva.html',{'reserva_lista': hospedes})
   })

def altera_reserva(request):
   if request.method == 'GET':
      id = request.GET.get('idReserva')
      print(id)
      nome = request.GET.get('nomeReserva') 
      cpf = request.GET.get('cpfReserva')
      telefone = request.GET.get('telefoneReserva')
      checkin = request.GET.get('checkinReserva')
      checkout = request.GET.get('checkoutReserva')

      reserva = Reserva.objects.get(id=id)
      
      reserva.id_hospede.nome = nome
      reserva.id_hospede.cpf = cpf
      reserva.id_hospede.telefone = telefone

      diff = (reserva.check_out - reserva.check_in).days
      reserva.diaria = diff
      
      reserva.save()

      if checkout != None:
         reserva.check_out = checkout

      reserva.check_in = checkin
      reserva.save()

      reserva = Reserva.objects.get(id=id)
      if reserva.check_out > date.today():
         reserva.is_active = True
      else:
         reserva.is_active = False
      reserva.save()

      return JsonResponse({"success": True, "message": "Reserva alterada com sucesso!"})
      # return JsonResponse({"message" : "Deu green"})
   return render(request, 'editar_reserva.html')

def deleta_reserva(request):
   if request.method == 'GET':
      id = request.GET.get('idReserva')
      print(id)
      
      reserva = Reserva.objects.get(id=id)
      
      quarto = Quarto.objects.get(num_quarto=reserva.num_quarto.num_quarto)
      quarto.disponibilidade = 3
      quarto.save()

      reserva.delete()
      return JsonResponse({"message" : "Apagou BLD"})
   return render(request, 'editar_reserva.html')

def fechar_reserva(request):
   if request.method == 'GET':
      id = request.GET.get('idReserva')
      print(id)
      
      reserva = Reserva.objects.get(id=id)
      reserva.is_active = False
      reserva.check_out = date.today()
      reserva.diaria = (reserva.check_in - reserva.check_out).days

      quarto = Quarto.objects.get(num_quarto=reserva.num_quarto.num_quarto)
      quarto.disponibilidade = 3

      quarto.save()
      reserva.save()
      return JsonResponse({"message" : "Apagou BLD"})
   return render(request, 'editar_reserva.html')

