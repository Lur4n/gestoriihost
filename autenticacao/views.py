from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from cadastros.models import Usuario

TOKENS = {}

def login(request):
    if request.method == 'POST':
        email = request.POST.get('txtEmail')
        senha = request.POST.get('txtSenha')
        perfil_id = request.POST.get('slcPerfil')

        print(email, senha, perfil_id)

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None and perfil_id:
            perfis_usuario = usuario.perfis.filter(id=perfil_id)
            if perfis_usuario.exists():
                #limpa as sessoes do usuario
                request.session.flush()
                #cria a sessao do usuario
                auth_login(request, usuario)
                
                request.session['nome'] = usuario.nome
                request.session['is_admin'] = usuario.is_admin
                # print(request.session['is_admin'])
                request.session['id_perfil'] = perfil_id
                request.session['id_atual'] = usuario.id
                request.session['email_atual'] = usuario.email                    
                request.session['perfil_atual'] = perfis_usuario.first().nome                
                request.session['perfis'] = list(usuario.perfis.values_list('nome', flat=True))
               #  request.session['quartos'] = Quarto.objects.filter(disponibilidade==).
                # print(request.session['perfis'])
                
                #configura sessao para expirar em 4 horas
                request.session.set_expiry(14400)
                
                messages.success(request, 'Login realizado com sucesso!')
                
                #no futuro iremos separar em diferentes paginas
                if request.session.get('perfil_atual') in {'Administrador', 'Funcionario'}:
                    return redirect('core:main')
                
            else:
                messages.error(request, 'Perfil inválido para este usuário.')
        else:
            if usuario is None:
                messages.error(request, 'Senha incorreta.')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
            
    return render(request, 'login.html')

def editar_perfil(request):
    messages.warning(request, 'Implementção Futura')
    return redirect ('core:main')

def get_perfis(request):
    email = request.GET.get('email', '')
    perfis = []
    if Usuario.objects.filter(email=email).exists():
        usuario = Usuario.objects.get(email=email)
        perfis = usuario.perfis.all().values('id', 'nome')
        data = {'perfis': list(perfis), 'usuario_existe': True}
    else:
        data = {'usuario_existe': False}
    return JsonResponse(data)

def logout(request):
    #limpa a sessao ao deslogar
    request.session.flush()
    auth_logout(request)
    
    messages.success(request, 'Logout realizado com sucesso.')
    return redirect('autenticacao:login')


#--------------Esqeci minha senha---------------#
def esqueci_senha(request):
   if request.method == 'POST':
      email = request.POST.get('email')
      if Usuario.objects.filter(email=email).exists():
         token = get_random_string(32)  # Gera um token aleatório
         TOKENS[token] = email  # Armazena o token e o username
         # Envia o e-mail com o token
         send_mail(
               'Recuperação de senha',
               f'Use este link para redefinir sua senha: '
               f'http://127.0.0.1:8000/recuperar_senha/{token}/',
               'gestoriihost@gmail.com',
               [email],
         )
         messages.success(request, 'E-mail enviado com sucesso.')
         return redirect('autenticacao:login')
      else:
         messages.error(request, 'E-mail não encontrado.')
         return redirect('autenticacao:login')
   return render(request, 'esqueci_senha.html')

def recuperar_senha(request, token):
   if request.method == 'POST':
      nova_senha = request.POST.get('senha')
      email = TOKENS.get(token)
      print(email)
      if email:
         user = Usuario.objects.get(email=email)
         user.password = make_password(nova_senha)
         user.save()
         del TOKENS[token]  # Remove o token após o uso
         messages.success(request, 'Senha alterada com sucesso.')
         return redirect('autenticacao:login')
      messages.error(request, 'Token inválido ou expirado.')
      return redirect('autenticacao:login')
   return render(request, 'recuperar_senha.html', {'token': token})