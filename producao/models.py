from django.contrib.auth.models import User
from django.db import models


class Usuario(models.Model):
    NIVEL_CHOICES = [
        ("ADMIM", "ADMIM"),
        ("GERENTE", "GERENTE"),
        ("OPERADOR", "OPERADOR"),
    ]

    id_usuario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    funcao = models.CharField(max_length=50, blank=True)
    nivel_acesso = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    usuario = models.CharField(max_length=50, unique=True)
    senha = models.CharField(max_length=100)

    class Meta:
        db_table = "cad_usuarios"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class PerfilUsuario(models.Model):
    NIVEL_CHOICES = [
        ("ADMIM", "ADMIM"),
        ("GERENTE", "GERENTE"),
        ("OPERADOR", "OPERADOR"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    funcao = models.CharField(max_length=50, blank=True)
    nivel_acesso = models.CharField(max_length=20, choices=NIVEL_CHOICES)

    class Meta:
        db_table = "perfis_usuarios"
        ordering = ["user__first_name", "user__username"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome_cliente = models.CharField(max_length=100, unique=True)
    cnpj = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = "cad_clientes"
        ordering = ["nome_cliente"]

    def __str__(self):
        return self.nome_cliente


class Item(models.Model):
    MEDIDAS_CHOICES = [
        ("BL", "BL"),
        ("TL", "TL"),
        ("M²", "M²"),
        ("CM", "CM"),
        ("UND", "UND"),
    ]

    id_item = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    p_12 = models.IntegerField(null=True, blank=True, db_column="P_12")
    descricao_item = models.CharField(max_length=300)
    medidas = models.CharField(max_length=10, choices=MEDIDAS_CHOICES)
    acabamento = models.CharField(max_length=300)

    class Meta:
        db_table = "cad_itens"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ("EM_PRODUCAO", "EM_PRODUCAO"),
        ("FINALIZADA", "FINALIZADA"),
        ("NF_EMITIDA", "NF_EMITIDA"),
        ("ENTREGUE", "ENTREGUE"),
    ]

    num_pedido = models.CharField(max_length=20, primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        to_field="nome_cliente",
        db_column="nome_cliente",
        on_delete=models.PROTECT,
        related_name="ordens",
    )
    status_geral = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="EM_PRODUCAO",
    )
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Ordem_servico"
        ordering = ["-data_criacao"]

    def __str__(self):
        return self.num_pedido


class OrdemServicoItem(models.Model):
    FASE_CHOICES = [
        ("PRE_IMPRESSAO", "Pre impressao"),
        ("IMPRESSAO", "Impressao"),
        ("CORTE", "Corte"),
        ("ACABAMENTO", "Acabamento"),
        ("EXPEDICAO", "Expedicao"),
        ("FINALIZADO", "Finalizado"),
    ]

    id_ordem_item = models.AutoField(primary_key=True)
    ordem = models.ForeignKey(
        OrdemServico,
        on_delete=models.CASCADE,
        related_name="itens_da_ordem",
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name="ordens",
    )
    quantidade = models.PositiveIntegerField(default=1)
    fase = models.CharField(
        max_length=20,
        choices=FASE_CHOICES,
        default="PRE_IMPRESSAO",
    )
    observacao = models.CharField(max_length=300, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ordem_servico_itens"
        ordering = ["ordem_id", "item__nome"]

    def __str__(self):
        return f"{self.ordem_id} - {self.item.nome}"
