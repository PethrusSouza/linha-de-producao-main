from .models import Cliente, Item, OrdemServico, OrdemServicoItem, PerfilUsuario, Usuario


class UsuarioRepository:
    @staticmethod
    def buscar_por_id(usuario_id):
        return Usuario.objects.filter(id_usuario=usuario_id).first()

    @staticmethod
    def autenticar(usuario_login, senha):
        return Usuario.objects.filter(usuario=usuario_login, senha=senha).first()

    @staticmethod
    def criar_admin_padrao():
        return Usuario.objects.create(
            nome="Administrador",
            funcao="Administrador",
            nivel_acesso="ADMIM",
            usuario="admin",
            senha="123",
        )

    @staticmethod
    def listar_todos():
        return PerfilUsuario.objects.select_related("user").all()


class ClienteRepository:
    @staticmethod
    def listar_todos():
        return Cliente.objects.all()


class ItemRepository:
    @staticmethod
    def listar_todos():
        return Item.objects.all()


class OrdemServicoRepository:
    @staticmethod
    def listar_recentes(limite=20):
        return OrdemServico.objects.select_related("cliente")[:limite]

    @staticmethod
    def buscar_por_numero(num_pedido):
        return OrdemServico.objects.select_related("cliente").filter(num_pedido=num_pedido).first()


class OrdemServicoItemRepository:
    @staticmethod
    def criar_itens_da_ordem(ordem, item_ids, quantidades, fases):
        itens_criados = []
        for index, item_id in enumerate(item_ids):
            if not item_id:
                continue

            quantidade = quantidades[index] if index < len(quantidades) else 1
            fase = fases[index] if index < len(fases) else "PRE_IMPRESSAO"
            try:
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                quantidade = 1

            itens_criados.append(
                OrdemServicoItem(
                    ordem=ordem,
                    item_id=item_id,
                    quantidade=quantidade or 1,
                    fase=fase or "PRE_IMPRESSAO",
                )
            )

        if itens_criados:
            OrdemServicoItem.objects.bulk_create(itens_criados)
        return itens_criados

    @staticmethod
    def listar_por_ordem(ordem):
        return OrdemServicoItem.objects.select_related("item", "ordem", "ordem__cliente").filter(ordem=ordem)

    @staticmethod
    def listar_em_producao():
        return OrdemServicoItem.objects.select_related("item", "ordem", "ordem__cliente").exclude(
            fase="FINALIZADO"
        )

    @staticmethod
    def buscar_por_id(item_id):
        return OrdemServicoItem.objects.select_related("item", "ordem").filter(
            id_ordem_item=item_id
        ).first()
