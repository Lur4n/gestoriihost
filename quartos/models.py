from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import ProtectedError

class Quarto(models.Model):
    numero = models.IntegerField()
    andar = models.IntegerField()
    descricao = models.CharField(max_length=500)
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    ocupado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Quarto {self.numero} - {self.andar}º andar"

# Create your models here.
