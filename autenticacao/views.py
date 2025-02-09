from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# from cadastros.models import Usuario
from django.http import JsonResponse

# Create your views here.
def login(request):
    email = request.POST.get('txtNome')
    if request.method == 'POST':
        if  email == 'adm':
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('core:main')
    #         # return render(request, 'lista_reservas.html')
     
            
    return render(request, 'login.html')

def logout(request):
    pass