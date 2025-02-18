from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordResetForm

class PasswordResetRequestForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, label="E-mail")
    
    class Meta:
        model = User
        fields = ['email']
