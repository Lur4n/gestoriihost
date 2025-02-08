from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from cadastros.models import Usuario
from django.http import JsonResponse

# Create your views here.
def login(request):
    email = request.POST.get('txtNome')
    if request.method == 'POST':
        if  email == 'adm':

            messages.success(request, 'Login realizado com sucesso!')

            return redirect('reservas:lista_reservas')


    #             request.session['id_atual'] = usuario.id
    #             request.session['email_atual'] = usuario.email
    #             request.session['departamento_id_atual'] = usuario.departamento.id
    #             request.session['departamento_nome_atual'] = usuario.departamento.nome
    #             request.session['departamento_sigla_atual'] = usuario.departamento.sigla
    #             request.session['perfil_atual'] = perfis_usuario.first().nome
    #             request.session['perfis'] = list(usuario.perfis.values_list('nome', flat=True))

    #             request.session.set_expiry(14400)

    #             messages.success(request, 'Login realizado com sucesso!')

    #             if request.session.get('perfil_atual') in {'Administrador', 'Estoquista', 'Vendedor'}:
    #                 return redirect('core:main')
    #         else:
    #             messages.error(request, 'Perfil Inválido')
    #     else:
    #         if usuario is None:
    #             messages.error(request, 'Senha errada!')
    #         else:
    #             messages.error(request, 'Usuario ou senha invalido!')

    return render(request, "login.html")


def mostruario(request):
    return render(request, "nossos_quartos.html")

def lista_reservas(request):
    messages.success(request, 'Deu boa de entrar na view de Reservas')
    return render(request, "lista_reservas.html")
