import os

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from producao.models import PerfilUsuario


class Command(BaseCommand):
    help = "Cria um superusuario a partir de variaveis de ambiente, se ele ainda nao existir."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not username or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_USERNAME ou DJANGO_SUPERUSER_PASSWORD nao configurado. Pulando criacao."
            )
            return

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": "Administrador",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )

        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' criado."))
        else:
            changed = False
            user.set_password(password)
            changed = True
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                changed = True
            if email and user.email != email:
                user.email = email
                changed = True
            if changed:
                user.save()
            self.stdout.write(f"Superusuario '{username}' ja existe.")

        grupo, _ = Group.objects.get_or_create(name="ADMIM")
        user.groups.add(grupo)
        PerfilUsuario.objects.get_or_create(
            user=user,
            defaults={
                "funcao": "Administrador",
                "nivel_acesso": "ADMIM",
            },
        )
