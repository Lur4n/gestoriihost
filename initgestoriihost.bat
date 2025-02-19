@echo off
:: Ativar o ambiente Conda
call conda activate gestoriihost

:: Rodar o servidor Django
start python manage.py runserver

:: Abrir o Google Chrome e acessar o endereço da aplicação
start chrome http://127.0.0.1:8000
