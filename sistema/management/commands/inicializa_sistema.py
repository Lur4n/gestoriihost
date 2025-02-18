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
         
      #--------------------------------- GERADOR DE DADOS ALEATÓRIOS ----------------------------------------

      # Instancia o gerador de dados aleatórios
      fake = faker.Faker()
      # O interessante dessa bib é que ela gera dados mais realistas, 
      # entao o campo de nome no modelo de hospedes, por exemplo, tem um
      # nome mais proximo do real, não uma sequencia de caracteres sem coerencia

      # Criação de 30 hóspedes aleatórios
      n_hosp = 30
      for _ in range(n_hosp):  # Insere 30 hóspedes
         # empresa aleatoria, ou nenhuma empresa
         empresa = fake.company() if random.choice([True, False]) else None
         # nome fake
         nome = fake.name()
         # gera CPF
         cpf = CPF.generate()
         # telefone fake sem caracteres nao numericos
         telefone = ''.join(filter(str.isdigit, fake.phone_number()))  # Remove qualquer caractere não numérico
         if len(telefone) > 11:
            telefone = telefone[:11]  #se vier um valor maior que 11 ele trunca pra 11

         #string de insert
         hospede = Hospede(empresa=empresa,nome=nome,cpf=cpf,telefone=telefone)
         #insert
         hospede.save()
         
      self.stdout.write(self.style.SUCCESS(f"[{n_hosp}] Hóspedes aleatorizados criados"))
      
      
      # Criação de 86 quartos aleatórios
      n_quarto = 80
      for i in range(n_quarto):  # Insere 86 quartos aleatórios
         num_quarto = i+1 #autoincrementando o quarto
         ranking = random.randint(1, 10) #aleatorizando o ranking
         descricao = f"Quarto {num_quarto} com características diversas." #padrao de descrição
         preco = round(random.uniform(50.0, 500.0), 2) # aleatorizando os precos de 50 a 500
         capacidade = random.randint(1, 4) # aleatorizando a capacidade
         disponibilidade = 1 # disponibilidade padrao, significa que o quarto esta livre

         # string de insert
         quarto = Quarto(
            num_quarto=num_quarto,
            ranking=ranking,
            descricao=descricao,
            preco=preco,
            capacidade=capacidade,
            disponibilidade=disponibilidade
         )
         # insert
         quarto.save()
      
      self.stdout.write(self.style.SUCCESS(f"[{n_quarto}] Quartos aleatorizados criados"))


      # pegando todos os quartos e hospedes
      quartos = Quarto.objects.all()
      hospedes = Hospede.objects.all()

      # pegando quartos aleatorios para colocar em manutenção
      for i in range(7):
         quarto = random.choice(quartos)# pegando um quarto aleatorio
         quarto.disponibilidade = 3 # disp. =3 significa, manutenção
         quarto.save()# salvando a alteração do quarto

      # Criação de 30 reservas aleatórias
      n_reservas = 30
      for _ in range(n_reservas):  # Insere 30 reservas
         hospede = random.choice(hospedes) # escolhendo hospedes aleatorios
         quarto = random.choice(quartos) # escolhendo quartos aleatorios
         # se o quarto ta livre ele vira ocupado
         if quarto.disponibilidade == 1:
            quarto.disponibilidade = 2 # recebendo o status de ocupado
            quarto.save()  # Salva o quarto no banco de dados

            # Gera as datas de check-in e check-out aleatórias
            check_in = fake.date_this_year()
            check_out = check_in + timedelta(days=random.randint(1, 7))
            

            # Gera observações aleatórias
            observacoes = fake.text(max_nb_chars=200)
            
            # Valor da diária aleatório
            diaria = (check_out - check_in).days

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
            
            # editando os status de atividade da reserva
            if date.today() > check_out:
               reserva.is_active = False

            reserva.save()  # Salva a reserva no banco de dados
      
      self.stdout.write(self.style.SUCCESS(f"[{n_reservas}] Reservas aleatorizadas criadas"))

