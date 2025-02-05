from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from cadastros.models import Usuario
from django.contrib import messages
from django.http import JsonResponse
from autenticacao import urls
from django.core.mail import EmailMessage

# Create your views here.
def login(request):
    # if request.method == 'POST':
    #     email = request.POST.get('txtEmail')
    #     senha = request.POST.get('txtSenha')
    #     perfil_id = request.POST.get('slcPerfil')

    #     usuario = authenticate(request, username=email, password=senha)

    #     if(usuario is not None and perfil_id):
    #         perfis_usuario = usuario.perfis.filter(id=perfil_id)
    #         if perfis_usuario.exists():
    #             request.session.flush()
    #             auth_login(request, usuario)

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
    
    return render(request, 'login.html')

def mostruario(request):
    return render(request, 'nossos_quartos.html')