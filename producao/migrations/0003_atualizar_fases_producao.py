from django.db import migrations, models


def migrar_fases_antigas(apps, schema_editor):
    OrdemServicoItem = apps.get_model("producao", "OrdemServicoItem")
    mapa_fases = {
        "AGUARDANDO": "PRE_IMPRESSAO",
        "ARTE": "PRE_IMPRESSAO",
        "IMPRESSAO": "IMPRESSAO",
        "ACABAMENTO": "ACABAMENTO",
        "CONFERENCIA": "EXPEDICAO",
        "FINALIZADO": "FINALIZADO",
    }

    for fase_antiga, fase_nova in mapa_fases.items():
        OrdemServicoItem.objects.filter(fase=fase_antiga).update(fase=fase_nova)


class Migration(migrations.Migration):
    dependencies = [
        ("producao", "0002_ordemservicoitem"),
    ]

    operations = [
        migrations.RunPython(migrar_fases_antigas, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="ordemservicoitem",
            name="fase",
            field=models.CharField(
                choices=[
                    ("PRE_IMPRESSAO", "Pre impressao"),
                    ("IMPRESSAO", "Impressao"),
                    ("CORTE", "Corte"),
                    ("ACABAMENTO", "Acabamento"),
                    ("EXPEDICAO", "Expedicao"),
                    ("FINALIZADO", "Finalizado"),
                ],
                default="PRE_IMPRESSAO",
                max_length=20,
            ),
        ),
    ]
