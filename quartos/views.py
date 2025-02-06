from django.shortcuts import render, redirect


# Create your views here.
def mostruario(request):
    return render(request, "nossos_quartos.html")
