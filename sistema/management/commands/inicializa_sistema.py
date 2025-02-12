from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cadastros.models import Perfil


class Command(BaseCommand):
    help = "Inicializa o sistema com dados padrão"

    def handle(self, *args, **options):
        # cria os perfis de usuarios
        perfil_administrador, created = Perfil.objects.get_or_create(
            id=1, nome="Administrador"
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Perfil criado: {perfil_administrador.nome}")
            )

        perfil_funcionario, created = Perfil.objects.get_or_create(
            id=2, nome="Funcionario"
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(f"Perfil criado: {perfil_funcionario.nome}")
            )

        # cria o usuario administrador principal do sistema
        User = get_user_model()
        User2 = get_user_model()
        if not User.objects.filter(email="adm@gmail.com").exists():
            usuario = User(
                email="adm@gmail.com",
                nome="Administrador",
                is_admin=True,
            )
            usuario2 = User2(
                email="ca@cu",
                nome="CACA",
                is_admin=False,
            )

            usuario.set_password("123456")
            usuario.save()

            usuario.perfis.add(perfil_administrador)
            usuario.save()

            usuario2.set_password(" ")
            usuario2.save()

            usuario2.perfis.add(perfil_funcionario)
            usuario2.save()

            self.stdout.write(self.style.SUCCESS("Usuario administrador criado"))
        else:
            self.stdout.write(self.style.WARNING("Usuario administrador já existe"))
