from django.shortcuts import render
from django.http import JsonResponse
from .models import Categoria, Produto, Estoque, Venda
from django.contrib import messages

def financeiro(request):
   return render(request, 'financeiro.html')

def produto(request):
   produtos = Produto.objects.all().order_by('categoria', '-id_produto')
   return render(request, 'produto.html', {'produtos': produtos})

def caixa(request):
   return render(request, 'caixa.html')
def estoque(request):
   return render(request, 'estoque.html')
def venda(request):
   return render(request, 'venda.html')


def categoria(request):
   categorias = Categoria.objects.all().order_by('-id')
   
   if request.method == 'POST':
      if request.POST.get('addNome') != '' and request.POST.get('addNome') != None:
         nome = request.POST.get('addNome')
         categoria = Categoria(nome=nome)
         categoria.save()
         messages.success(request, "Categoria adicionada com sucesso!")
      action = request.POST.get('action')
      nome_categoria = request.POST.get('nome')
      categoria_id = request.POST.get('linha')  # Você pode precisar de um campo oculto para o id, se necessário.

      if action == 'atualizar':
         # Atualizar a categoria
         categoria = Categoria.objects.get(id=categoria_id)
         categoria.nome = nome_categoria
         categoria.save()
         messages.success(request, "Categoria atualizada com sucesso!")

      elif action == 'apagar':
         # Apagar a categoria
         categoria = Categoria.objects.get(id=categoria_id)
         categoria.delete()
         messages.success(request, "Categoria apagada com sucesso!")

   return render(request, 'categoria.html', {'lista_categoria': categorias})

def criar_categoria(request):
   pass

def criar_produto(request):
   pass

def criar_estoque(request):
   pass

def criar_venda(request):
   pass

def listar_vendas(request):
   pass

# Compare this snippet from financeiro/admin.py:
