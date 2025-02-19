from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Hospede, Reserva
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.shortcuts import get_object_or_404
from datetime import datetime


@login_required
def criar_hospede(request):
   if request.method =='POST':
      nome = request.POST.get('txtNome')
      empresa = request.POST.get('txtEmpresa')
      telefone = request.POST.get('txtTelefone')
      cpf = request.POST.get('txtCpf')

      hospede = Hospede(
         nome=nome,
         empresa=empresa,
         telefone=telefone,
         cpf=cpf
      )
      hospede.save()
      messages.success(request, f'{nome} com sucesso')
      return redirect('core:main')
   return render(request, 'criar_hospede.html')

def busca_hospede(request):
   hospede_nome = request.GET.get('hospede_nome', '')
   hospede_cpf = request.GET.get('hospede_cpf', '')
   if hospede_nome:
      hospedes = Hospede.objects.filter(nome__icontains=hospede_nome).values('nome', 'cpf','telefone', 'empresa')[:10]
      print('Passou aq com: ', hospede_nome)
      for hospede in hospedes:
         print(hospede)
   elif hospede_cpf:
      hospedes = Hospede.objects.filter(cpf__icontains=hospede_cpf).values('nome', 'cpf', 'telefone', 'empresa')[:10]
      print('Passou aq com: ', hospede_nome)
      for hospede in hospedes:
         print(hospede)
   else:
      hospedes = []
      print("vazio")
   return JsonResponse({'hospedes': list(hospedes)})


#-------------- RESERVA ----------------------#
@login_required
def criar_reserva(request):

   quartos = Quarto.objects.filter(disponibilidade=1).order_by('-ranking').values_list('num_quarto', flat = True)

   if request.method =='POST':
      nome = request.POST.get('txtNomeReserva')
      empresa = request.POST.get('txtEmpresaReserva')
      telefone = request.POST.get('txtTelefoneReserva')
      cpf = request.POST.get('txtCpfReserva')
      checkin = request.POST.get('dateCheckin')
      checkout = request.POST.get('dateCheckout')
      num_quarto = request.POST.get('num_quarto')

      print(checkout)
      if(checkout==""):
         print(checkout)
         checkout = None

      if (nome=="" or checkin=="" or cpf=="" or num_quarto==""):
         messages.error(request, f'O Nome, Checkin e CPF São Obrigatorios')
         return render(request, 'criar_reserva.html', {'quartos': quartos})
      
      if not Hospede.objects.filter(cpf=cpf).exists():
         hospede = Hospede(
         nome=nome,
         empresa=empresa,
         telefone=telefone,
         cpf=cpf
         )
         hospede.save()
   
      hospede = Hospede.objects.get(cpf=cpf)
      quarto = Quarto.objects.get(num_quarto=num_quarto)
      

      check_out = datetime.strptime(checkout, '%Y-%m-%d')
      check_in = datetime.strptime(checkin, '%Y-%m-%d')
      diff = (check_out - check_in).days
      if diff < 0:
         diff = diff *-1

      total = diff * quarto.preco

      reserva = Reserva(
         check_in = checkin,
         check_out = checkout,
         id_hospede = hospede,
         num_quarto = quarto,
         is_active = 1,
         diaria = diff,
         total = total
      )
      
      quarto.disponibilidade = 2

      quarto.save()
      reserva.save()
      messages.success(request, f'Reserva salva com sucesso')
      return redirect('reservas:reservas')
   
   return render(request, 'criar_reserva.html', {'quartos': quartos, 'total': quartos.count()})


#-------------------- CRUD QUARTOS ------------------#

@login_required
def criar_quarto(request):
   if request.session.get('perfil_atual') not in {'Administrador'}:
      messages.error(request, "Você não é administrador!")
      return redirect('core:main')
   
   if request.method == 'POST':
      capacidade = request.POST.get('numCapacidade')
      numero = request.POST.get('numNumero')
      preco = request.POST.get('numPreco')
      ranking = request.POST.get('numCapacidade')
      disponibilidade = request.POST.get('numDisponibilidade')
      descricao = request.POST.get('txtAreaDesc')

      if not Quarto.objects.filter(num_quarto=numero).exists():
            
            quarto = Quarto(
               num_quarto=numero,
               ranking=ranking,
               descricao=descricao,
               preco=preco,
               capacidade=capacidade,
               disponibilidade=disponibilidade
            )
            quarto.save()
            messages.success(request, 'Quarto salvo com sucesso!')
            return redirect('cadastros:criar_quarto')
      else:
         messages.success(request, {'O número já esta sendo usado!'})

      # messages.success(request, {'Cap':capacidade, 'num':numero, 'preco':preco, 'disponibilidade':disponibilidade, 'ranking':ranking, 'descricao':descricao})

   return render(request, 'criar_quarto.html')

@login_required
def apagar_quarto(request):
   if request.session.get('perfil_atual') not in {'Administrador'}:
      messages.error(request, "Você não é administrador!")
      return redirect('core:main')
   
   try:
      num_quarto = request.GET.get('num_quarto')
      quarto = get_object_or_404(Quarto, num_quarto=num_quarto)
      quarto.delete()
      return JsonResponse({"message": "Quarto apagado com sucesso!"})
   except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)

def busca_quarto_id(request):
   # Verifica se o parâmetro 'num_quarto' foi fornecido
   num_quarto = request.GET.get('num_quarto', '')
    
   if num_quarto:
      # Filtra os quartos com base no número fornecido
      quarto = Quarto.objects.filter(num_quarto=num_quarto).values()
      
      if quarto.exists():
         return JsonResponse({'quarto': list(quarto)})  # Utiliza .values() para retornar apenas dados serializáveis
      else:
         return JsonResponse({'message': 'Nenhum quarto encontrado'})
   else:
      # Caso o parâmetro 'num_quarto' não seja fornecido
      print('Número de quarto não fornecido.')
      return JsonResponse({'message': 'Número de quarto não fornecido'})

@login_required
def editar_quarto(request):
   if request.session.get('perfil_atual') not in {'Administrador'}:
      messages.error(request, "Você não é administrador!")
      return redirect('core:main')
   
   quartos = Quarto.objects.all().order_by('num_quarto')
   page_number = request.GET.get('page')
   paginator = Paginator(quartos, settings.NUMBER_GRID_PAGES)

   if request.method == 'POST':
      if request.POST.get('txtEditaNumQuarto'):
         num_quarto = request.POST.get('txtEditaNumQuarto')
         ranking = request.POST.get('txtEditaRanking')
         preco = request.POST.get('txtEditaPreco')
         capacidade = request.POST.get('txtEditaCapacidade')
         disponibilidade = request.POST.get('disponibilidade')

         try:
            quarto = Quarto.objects.get(num_quarto=num_quarto)
         except Quarto.DoesNotExist:
            messages.error(request, f'Quarto com número {num_quarto} não encontrado.')
            return redirect('cadastros:editar_quarto')

         # Converte os valores recebidos para os tipos corretos
         try:
            ranking = int(ranking) if ranking else None  # Se vazio, define como None
         except ValueError:
            ranking = None

         try:
            preco = float(preco) if preco else None  # Se vazio, define como None
         except ValueError:
            preco = None

         try:
            capacidade = int(capacidade) if capacidade else None  # Se vazio, define como None
         except ValueError:
            capacidade = None

         # Verifica a disponibilidade
         if disponibilidade not in ['1', '2', '3']:
            disponibilidade = None  # Se a opção de disponibilidade não for válida, define como None

         # Compara os valores atuais com os novos valores
         modificado = False

         if quarto.ranking != ranking:
            quarto.ranking = ranking
            modificado = True
         if quarto.preco != preco:
            quarto.preco = preco
            modificado = True
         if quarto.capacidade != capacidade:
            quarto.capacidade = capacidade
            modificado = True
         if quarto.disponibilidade != int(disponibilidade):
            quarto.disponibilidade = int(disponibilidade)
            modificado = True

         # Se houve alguma modificação, salva no banco de dados
         if modificado:
            quarto.save()
            messages.success(request, f'Quarto número {num_quarto} atualizado com sucesso!')
         else:
            messages.info(request, 'Nenhuma alteração foi feita no quarto.')
      else:
         messages.info(request, 'Selecione um quarto clicando sobre ele')
   page_obj = paginator.get_page(page_number)
   return render(request, 'editar_quarto.html', {'quarto_lista': quartos, 'page_obj': page_obj})

#------------------------- Hóspede --------------------------#

def editar_hospede(request):
   if request.session.get('perfil_atual') not in {'Administrador'}:
      messages.error(request, "Você não é administrador!")
      return redirect('core:main')
   
   hospede = Hospede.objects.all().order_by('-id')
   page_number = request.GET.get('page')
   paginator = Paginator(hospede, settings.NUMBER_GRID_PAGES) 
   if request.method == 'POST':
      id = request.POST.get('id_hospede')
      nome = request.POST.get('txtEditaNome')
      cpf = request.POST.get('txtEditaCpf')
      empresa = request.POST.get('txtEditaEmpresa')
      telefone = request.POST.get('txtEditaTelefone')

      if id:
         try:
            hospede = Hospede.objects.get(id=id)
            print("hospede: ", hospede)
         except Hospede.DoesNotExist:
            messages.error(request, f'Hospede com número {id} não encontrado.')
            return redirect('cadastros:editar_hospede')
         
         modificado = False

         if hospede.nome != nome:
            hospede.nome = nome
            modificado = True 
         if hospede.cpf != cpf:
            hospede.cpf = cpf
            modificado = True
         if hospede.empresa != empresa:
            hospede.empresa = empresa
            modificado = True
         if hospede.telefone != telefone:
            hospede.telefone = telefone
            modificado = True

         if modificado:
            hospede.save()
            messages.success(request, f'O hospede {nome} atualizado com sucesso!')
         else:
            messages.success(request, 'Nenhuma alteração foi feita no quarto')
         
      else:
         messages.info(request, 'Selecione um hóspede clicando sobre ele')
         

   page_obj = paginator.get_page(page_number)
   # tamListaHospedes = hospede.objects.count()
   return render(request, 'editar_hospede.html', {'hospedes': hospede, 'page_obj': page_obj})


@login_required
def apagar_hospede(request):
   if request.session.get('perfil_atual') not in {'Administrador'}:
      messages.error(request, "Você não é administrador!")
      return redirect('core:main')
   
   try:
      id_hospede = request.GET.get('id_hospede')
      hospede = get_object_or_404(Hospede, id=id_hospede)
      hospede.delete()
      return JsonResponse({"message": "Hóspede apagado com sucesso!"})
   
   except Exception as e:
      return JsonResponse({"error": str(e)}, status=500)
   
def busca_hospede_id(request):
   # Verifica se o parâmetro 'num_hospede' foi fornecido
   num_hospede = request.GET.get('id_hospede', '')
    
   if num_hospede:
      # Filtra os hospedes com base no id fornecido
      hospede = Hospede.objects.filter(id=num_hospede).values()
      
      if hospede.exists():
         return JsonResponse({'hospede': list(hospede)})  # Utiliza .values() para retornar apenas dados serializáveis
      else:
         return JsonResponse({'message': 'Nenhum hospede encontrado'})
   else:
      # Caso o parâmetro 'num_hospede' não seja fornecido
      print('Número de hospede não fornecido.')
      return JsonResponse({'message': 'Id de hospede não fornecido'})