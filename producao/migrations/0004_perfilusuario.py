from django.contrib.auth.hashers import make_password
from django.db import migrations, models
import django.db.models.deletion


def migrar_usuarios_legados(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    User = apps.get_model("auth", "User")
    Usuario = apps.get_model("producao", "Usuario")
    PerfilUsuario = apps.get_model("producao", "PerfilUsuario")

    for nome_grupo in ["ADMIM", "GERENTE", "OPERADOR"]:
        Group.objects.get_or_create(name=nome_grupo)

    for usuario_legado in Usuario.objects.all():
        user, criado = User.objects.get_or_create(
            username=usuario_legado.usuario,
            defaults={
                "password": make_password(usuario_legado.senha),
                "first_name": usuario_legado.nome.split(" ", 1)[0],
                "last_name": usuario_legado.nome.split(" ", 1)[1]
                if " " in usuario_legado.nome
                else "",
                "is_active": True,
                "is_staff": usuario_legado.nivel_acesso == "ADMIM",
                "is_superuser": usuario_legado.nivel_acesso == "ADMIM",
            },
        )

        if not criado and not user.has_usable_password():
            user.password = make_password(usuario_legado.senha)
            user.save(update_fields=["password"])

        perfil, _ = PerfilUsuario.objects.get_or_create(
            user=user,
            defaults={
                "funcao": usuario_legado.funcao,
                "nivel_acesso": usuario_legado.nivel_acesso,
            },
        )

        grupo = Group.objects.get(name=perfil.nivel_acesso)
        user.groups.add(grupo)

    if not User.objects.filter(username="admin").exists():
        admin = User.objects.create(
            username="admin",
            password=make_password("123"),
            first_name="Administrador",
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        PerfilUsuario.objects.create(
            user=admin,
            funcao="Administrador",
            nivel_acesso="ADMIM",
        )
        admin.groups.add(Group.objects.get(name="ADMIM"))


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("producao", "0003_atualizar_fases_producao"),
    ]

    operations = [
        migrations.CreateModel(
            name="PerfilUsuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("funcao", models.CharField(blank=True, max_length=50)),
                (
                    "nivel_acesso",
                    models.CharField(
                        choices=[
                            ("ADMIM", "ADMIM"),
                            ("GERENTE", "GERENTE"),
                            ("OPERADOR", "OPERADOR"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="perfil",
                        to="auth.user",
                    ),
                ),
            ],
            options={
                "db_table": "perfis_usuarios",
                "ordering": ["user__first_name", "user__username"],
            },
        ),
        migrations.RunPython(migrar_usuarios_legados, migrations.RunPython.noop),
    ]
