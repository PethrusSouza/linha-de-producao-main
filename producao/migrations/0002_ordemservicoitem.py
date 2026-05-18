from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("producao", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrdemServicoItem",
            fields=[
                ("id_ordem_item", models.AutoField(primary_key=True, serialize=False)),
                ("quantidade", models.PositiveIntegerField(default=1)),
                (
                    "fase",
                    models.CharField(
                        choices=[
                            ("AGUARDANDO", "Aguardando"),
                            ("ARTE", "Arte"),
                            ("IMPRESSAO", "Impressao"),
                            ("ACABAMENTO", "Acabamento"),
                            ("CONFERENCIA", "Conferencia"),
                            ("FINALIZADO", "Finalizado"),
                        ],
                        default="AGUARDANDO",
                        max_length=20,
                    ),
                ),
                ("observacao", models.CharField(blank=True, max_length=300)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="ordens",
                        to="producao.item",
                    ),
                ),
                (
                    "ordem",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="itens_da_ordem",
                        to="producao.ordemservico",
                    ),
                ),
            ],
            options={
                "db_table": "ordem_servico_itens",
                "ordering": ["ordem_id", "item__nome"],
            },
        ),
    ]
