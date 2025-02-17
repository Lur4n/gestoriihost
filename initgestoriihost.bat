@echo off
:: Ativar o ambiente Conda
call conda activate gestoriihost

:: Rodar o servidor Django
python manage.py runserver