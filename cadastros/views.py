from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cadastros.models import Quarto, Hospede, Reserva
from django.contrib import messages
from django.http import JsonResponse

def criar_reserva(request):
   
   return render(request, 'criar_reserva.html')

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

def criar_quarto(request):

   return render(request, 'criar_quarto.html')

# departamento_nome = request.GET.get('departamento_nome', '')
#     numero_pagina = request.GET.get('page')

#     departamento_lista = Departamento.objects.filter(nome__icontains=departamento_nome).exclude(nome__iexact="Geral").order_by('nome')

#     paginator = Paginator(departamento_lista, settings.NUMBER_GRID_PAGES)
#     page_obj = paginator.get_page(numero_pagina)

#     return JsonResponse({
#         'html': render_to_string('departamentos_table.html', {'page_obj': page_obj, 'query': departamento_nome, 'request': request})
#     })

def busca_hospede(request):
   nome = request.GET.get('hospede_nome', '')
   hospede = Hospede.objects.filter(nome__icontains=nome)
   print(nome)

   return JsonResponse({'hospede': hospede})