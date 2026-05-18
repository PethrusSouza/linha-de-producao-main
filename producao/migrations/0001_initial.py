from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cliente",
            fields=[
                ("id_cliente", models.AutoField(primary_key=True, serialize=False)),
                ("nome_cliente", models.CharField(max_length=100, unique=True)),
                ("cnpj", models.CharField(blank=True, max_length=20)),
                ("endereco", models.CharField(blank=True, max_length=50)),
            ],
            options={
                "db_table": "cad_clientes",
                "ordering": ["nome_cliente"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id_item", models.AutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=100)),
                ("p_12", models.IntegerField(blank=True, db_column="P_12", null=True)),
                ("descricao_item", models.CharField(max_length=300)),
                (
                    "medidas",
                    models.CharField(
                        choices=[
                            ("BL", "BL"),
                            ("TL", "TL"),
                            ("M²", "M²"),
                            ("CM", "CM"),
                            ("UND", "UND"),
                        ],
                        max_length=10,
                    ),
                ),
                ("acabamento", models.CharField(max_length=300)),
            ],
            options={
                "db_table": "cad_itens",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("id_usuario", models.AutoField(primary_key=True, serialize=False)),
                ("nome", models.CharField(max_length=50)),
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
                ("usuario", models.CharField(max_length=50, unique=True)),
                ("senha", models.CharField(max_length=100)),
            ],
            options={
                "db_table": "cad_usuarios",
                "ordering": ["nome"],
            },
        ),
        migrations.CreateModel(
            name="OrdemServico",
            fields=[
                ("num_pedido", models.CharField(max_length=20, primary_key=True, serialize=False)),
                (
                    "status_geral",
                    models.CharField(
                        choices=[
                            ("EM_PRODUCAO", "EM_PRODUCAO"),
                            ("FINALIZADA", "FINALIZADA"),
                            ("NF_EMITIDA", "NF_EMITIDA"),
                            ("ENTREGUE", "ENTREGUE"),
                        ],
                        default="EM_PRODUCAO",
                        max_length=20,
                    ),
                ),
                ("data_criacao", models.DateTimeField(auto_now_add=True)),
                (
                    "cliente",
                    models.ForeignKey(
                        db_column="nome_cliente",
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ordens",
                        to="producao.cliente",
                        to_field="nome_cliente",
                    ),
                ),
            ],
            options={
                "db_table": "Ordem_servico",
                "ordering": ["-data_criacao"],
            },
        ),
    ]
