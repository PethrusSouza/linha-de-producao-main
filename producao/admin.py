from django.contrib import admin

from .models import Cliente, Item, OrdemServico, OrdemServicoItem, PerfilUsuario, Usuario


admin.site.register(Cliente)
admin.site.register(Item)
admin.site.register(OrdemServico)
admin.site.register(OrdemServicoItem)
admin.site.register(PerfilUsuario)
admin.site.register(Usuario)
