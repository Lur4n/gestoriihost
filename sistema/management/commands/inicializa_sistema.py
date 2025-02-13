from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cadastros.models import Perfil, Quarto, Hospede, Reserva
import random
from datetime import timedelta, date
import faker  # Biblioteca para gerar dados aleatórios realistas
from cpf_generator import CPF  # Gerador de CPF válido


class Command(BaseCommand):
   help = "Inicializa o sistema com dados padrão"

   def handle(self, *args, **options):
      # Cria os perfis de usuários
      perfil_administrador, created = Perfil.objects.get_or_create(id=1, nome="Administrador")
      if created:
         self.stdout.write(self.style.SUCCESS(f"Perfil criado: {perfil_administrador.nome}"))

      perfil_funcionario, created = Perfil.objects.get_or_create(id=2, nome="Funcionario")
      if created:
         self.stdout.write(self.style.SUCCESS(f"Perfil criado: {perfil_funcionario.nome}"))

      # Cria o usuário administrador principal do sistema
      User = get_user_model()
      if not User.objects.filter(email="adm@gmail.com").exists():
         usuario = User(
               email="adm@gmail.com",
               nome="Administrador",
               is_admin=True,
         )
         usuario2 = User(
               email="ca@cu",
               nome="CACA",
               is_admin=False,
         )

         usuario.set_password("123456")
         usuario.save()
         usuario.perfis.add(perfil_administrador)
         usuario.save()

         usuario2.set_password(" ")  # Ajuste para garantir que a senha não seja vazia
         usuario2.save()
         usuario2.perfis.add(perfil_funcionario)
         usuario2.save()

         self.stdout.write(self.style.SUCCESS("Usuário administrador criado"))

      else:
         self.stdout.write(self.style.WARNING("Usuário administrador já existe"))

      # Instancia o gerador de dados aleatórios
      fake = faker.Faker()

      # Criação de 30 hóspedes aleatórios
      for _ in range(30):  # Insere 30 hóspedes
         empresa = fake.company() if random.choice([True, False]) else None
         nome = fake.name()

         # Gerando um CPF válido
         cpf = CPF.generate()  # Gerar um CPF válido

         telefone = ''.join(filter(str.isdigit, fake.phone_number()))  # Remove qualquer caractere não numérico
         if len(telefone) > 11:
            telefone = telefone[:11]  

         hospede = Hospede(
               empresa=empresa,
               nome=nome,
               cpf=cpf,
               telefone=telefone
         )
         hospede.save()
      
      
      # Criação de 30 quartos aleatórios
      for i in range(86):  # Insere 30 quartos
         num_quarto = i+1
         ranking = random.randint(1, 5)
         descricao = f"Quarto {num_quarto} com características diversas."
         preco = round(random.uniform(50.0, 500.0), 2)
         capacidade = random.randint(1, 4)
         disponibilidade = 1

         quarto = Quarto(
               num_quarto=num_quarto,
               ranking=ranking,
               descricao=descricao,
               preco=preco,
               capacidade=capacidade,
               disponibilidade=disponibilidade
         )
         quarto.save()

      quartos = Quarto.objects.all()
      hospedes = Hospede.objects.all()

      for i in range(7):
         quarto = random.choice(quartos)
         quarto.disponibilidade = 3
         quarto.save()

      # Criação de 30 reservas aleatórias
      for _ in range(30):  # Insere 30 reservas
         hospede = random.choice(hospedes)
         quarto = random.choice(quartos)
         if quarto.disponibilidade == 1:
            quarto.disponibilidade = 2

            # Gera as datas de check-in e check-out aleatórias
            check_in = fake.date_this_year()
            check_out = check_in + timedelta(days=random.randint(1, 7))
            
            # Gera o valor da diária aleatório
            diaria = random.randint(100, 500)

            # Gera observações aleatórias
            observacoes = fake.text(max_nb_chars=200)

            # Calcula o total da reserva
            total = diaria * (check_out - check_in).days

            # Quantidade de pessoas na reserva
            quant_pessoas = random.randint(1, 4)

            # Cria e salva a reserva
            reserva = Reserva(
                  check_in=check_in,
                  check_out=check_out,
                  diaria=diaria,
                  observacoes=observacoes,
                  total=total,
                  pago=random.choice([True, False]),  # Aleatoriamente True ou False
                  quant_pessoas=quant_pessoas,
                  id_hospede=hospede,
                  num_quarto=quarto
            )
            
            if date.today() > check_out:
               reserva.is_active = False

            reserva.save()  # Salva a reserva no banco de dados
            quarto.save()  # Salva o quarto no banco de dados

      self.stdout.write(self.style.SUCCESS("30 Reservas Aleatorizadas criadas"))
      self.stdout.write(self.style.SUCCESS("86 Quartos Aleatorizados criados"))
      self.stdout.write(self.style.SUCCESS("30 Hóspedes Aleatorizados criados"))
