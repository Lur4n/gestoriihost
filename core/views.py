from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def main(request):
    return render(request, "lista_reserva.html")
