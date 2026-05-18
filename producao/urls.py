from django.urls import path

from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/<str:num_pedido>/", views.ordem_detalhe, name="ordem_detalhe"),
    path("painel-producao/", views.painel_producao, name="painel_producao"),
    path("painel-producao/item/<int:item_id>/fase/", views.atualizar_fase_item, name="atualizar_fase_item"),
    path("clientes/", views.clientes, name="clientes"),
    path("itens/", views.itens, name="itens"),
    path("usuarios/", views.usuarios, name="usuarios"),
    path("logout/", views.logout_view, name="logout"),
]
