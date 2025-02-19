from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Usuario, Reserva, Hospede
from django.template.loader import render_to_string
from django.http import JsonResponse
from datetime import date, datetime
@login_required
def reservas(request):

   if request.method == 'POST':
      num_quarto = request.POST.get('num_quarto')#associando o valor do input ao num_quarto la reservas.html
      reserva_unica = Reserva.objects.filter(num_quarto=num_quarto).order_by("-id")#filtrando por quarto
      
      if reserva_unica.exists():#se existir essa reserva unica
         messages.error(request, f"Reserva já existente para o quarto {num_quarto}.")
         return render(request, 'reservas.html', {'reserva_lista': reserva_unica})#renderiza a reserva.html com a {reserva_lista: reserva_unica}
      else:#se nao 
         messages.success(request, f"Quarto {num_quarto} disponível para nova reserva.")

   reserva_lista = Reserva.objects.all().order_by("-is_active", "-id")#pega os quartos
   return render(request, 'reservas.html', {'reserva_lista': reserva_lista, 'total': reserva_lista.count()})

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
      checkin = datetime.strptime(checkin, "%Y-%m-%d")
      
      checkout = request.GET.get('checkoutReserva')
      checkout = datetime.strptime(checkout, "%Y-%m-%d")

      reserva = Reserva.objects.get(id=id)

      reserva.check_in = checkin
      reserva.check_out = checkout
      reserva.save()
      
      reserva = Reserva.objects.get(id=id)

      diff = (reserva.check_out - reserva.check_in).days
      reserva.diaria = diff
      
      reserva.total = round(reserva.diaria*reserva.num_quarto.preco, 2)
      reserva.save()

      reserva = Reserva.objects.get(id=id)
      
      reserva.id_hospede.nome = nome
      reserva.id_hospede.cpf = cpf
      reserva.id_hospede.telefone = telefone

      # if checkout != None:
      #    reserva.check_out = checkout

      # reserva.check_in = checkin
      
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
      checkin = request.GET.get('checkinReserva')
      checkout = request.GET.get('checkoutReserva')
      
      reserva = Reserva.objects.get(id=id)
      reserva.is_active = False
      reserva.check_out = date.today()
      reserva.diaria = (reserva.check_in - reserva.check_out).days
      if reserva.diaria < 0:
         reserva.diaria *= -1

      quarto = Quarto.objects.get(num_quarto=reserva.num_quarto.num_quarto)
      quarto.disponibilidade = 3

      reserva.total = reserva.diaria * quarto.preco
      if reserva.total < 0:
         reserva.total *= -1
      quarto.save()
      reserva.save()
      return JsonResponse({"message" : "Apagou BLD"})
   return render(request, 'editar_reserva.html')

