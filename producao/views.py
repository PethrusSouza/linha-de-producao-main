from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import (
    AtualizarFaseItemForm,
    ClienteForm,
    ItemForm,
    LoginForm,
    OrdemServicoForm,
    OrdemServicoItemForm,
    UsuarioForm,
)
from .repositories import (
    ClienteRepository,
    ItemRepository,
    OrdemServicoItemRepository,
    OrdemServicoRepository,
    UsuarioRepository,
)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.cleaned_data["user"])
        return redirect("dashboard")

    return render(request, "index.html", {"form": form})


def logout_view(request):
    auth_logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    form = OrdemServicoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ordem = form.save()
        itens_criados = OrdemServicoItemRepository.criar_itens_da_ordem(
            ordem=ordem,
            item_ids=request.POST.getlist("itens"),
            quantidades=request.POST.getlist("quantidades"),
            fases=request.POST.getlist("fases"),
        )

        if itens_criados:
            messages.success(request, "Ordem de servico cadastrada com itens.")
        else:
            messages.success(request, "Ordem de servico cadastrada sem itens.")
        return redirect("dashboard")

    ordens = OrdemServicoRepository.listar_recentes()
    return render(
        request,
        "dashboard.html",
        {
            "form": form,
            "ordens": ordens,
            "itens_catalogo": ItemRepository.listar_todos(),
            "fases_item": OrdemServicoItemForm.Meta.model.FASE_CHOICES,
        },
    )


@login_required
def ordem_detalhe(request, num_pedido):
    ordem = OrdemServicoRepository.buscar_por_numero(num_pedido)
    if not ordem:
        messages.error(request, "Ordem de servico nao encontrada.")
        return redirect("dashboard")

    form = OrdemServicoItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ordem_item = form.save(commit=False)
        ordem_item.ordem = ordem
        ordem_item.save()
        messages.success(request, "Item adicionado a ordem de servico.")
        return redirect("ordem_detalhe", num_pedido=ordem.num_pedido)

    return render(
        request,
        "ordem_detalhe.html",
        {
            "ordem": ordem,
            "form": form,
            "itens_da_ordem": OrdemServicoItemRepository.listar_por_ordem(ordem),
        },
    )


@login_required
def painel_producao(request):
    return render(
        request,
        "painel_producao.html",
        {
            "itens_producao": OrdemServicoItemRepository.listar_em_producao(),
            "fase_form": AtualizarFaseItemForm(),
        },
    )


@login_required
def atualizar_fase_item(request, item_id):
    ordem_item = OrdemServicoItemRepository.buscar_por_id(item_id)
    if not ordem_item:
        messages.error(request, "Item da ordem nao encontrado.")
        return redirect("painel_producao")

    form = AtualizarFaseItemForm(request.POST or None, instance=ordem_item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fase atualizada.")

    origem = request.POST.get("origem")
    if origem == "ordem":
        return redirect("ordem_detalhe", num_pedido=ordem_item.ordem.num_pedido)
    return redirect("painel_producao")


@login_required
def clientes(request):
    form = ClienteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Cliente cadastrado com sucesso.")
        return redirect("clientes")

    return render(
        request,
        "clientes.html",
        {"form": form, "clientes": ClienteRepository.listar_todos()},
    )


@login_required
def itens(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Item cadastrado com sucesso.")
        return redirect("itens")

    return render(
        request,
        "itens.html",
        {"form": form, "itens": ItemRepository.listar_todos()},
    )


@login_required
def usuarios(request):
    form = UsuarioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Usuario cadastrado com sucesso.")
        return redirect("usuarios")

    return render(
        request,
        "usuarios.html",
        {"form": form, "usuarios": UsuarioRepository.listar_todos()},
    )
