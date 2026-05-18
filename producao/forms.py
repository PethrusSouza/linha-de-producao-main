from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User

from .models import Cliente, Item, OrdemServico, OrdemServicoItem, PerfilUsuario


class LoginForm(forms.Form):
    usuario = forms.CharField(label="Usuario")
    senha = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        senha = cleaned_data.get("senha")

        if usuario and senha:
            user = authenticate(username=usuario, password=senha)
            if not user:
                raise forms.ValidationError("Usuario ou senha invalidos.")
            if not user.is_active:
                raise forms.ValidationError("Este usuario esta inativo.")
            cleaned_data["user"] = user

        return cleaned_data


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["nome", "p_12", "medidas", "descricao_item", "acabamento"]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome_cliente", "cnpj", "endereco"]


class UsuarioForm(forms.Form):
    NIVEL_CHOICES = PerfilUsuario.NIVEL_CHOICES

    nome = forms.CharField(max_length=150)
    funcao = forms.CharField(max_length=50, required=False)
    usuario = forms.CharField(max_length=150)
    nivel_acesso = forms.ChoiceField(choices=NIVEL_CHOICES)
    senha = forms.CharField(widget=forms.PasswordInput)

    def clean_usuario(self):
        usuario = self.cleaned_data["usuario"]
        if User.objects.filter(username=usuario).exists():
            raise forms.ValidationError("Este usuario ja existe.")
        return usuario

    def save(self):
        nome = self.cleaned_data["nome"].strip()
        partes_nome = nome.split(" ", 1)
        first_name = partes_nome[0]
        last_name = partes_nome[1] if len(partes_nome) > 1 else ""

        user = User.objects.create_user(
            username=self.cleaned_data["usuario"],
            password=self.cleaned_data["senha"],
            first_name=first_name,
            last_name=last_name,
        )

        perfil = PerfilUsuario.objects.create(
            user=user,
            funcao=self.cleaned_data["funcao"],
            nivel_acesso=self.cleaned_data["nivel_acesso"],
        )

        grupo, _ = Group.objects.get_or_create(name=self.cleaned_data["nivel_acesso"])
        user.groups.add(grupo)
        return perfil


class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ["num_pedido", "cliente", "status_geral"]


class OrdemServicoItemForm(forms.ModelForm):
    class Meta:
        model = OrdemServicoItem
        fields = ["item", "quantidade", "fase", "observacao"]


class AtualizarFaseItemForm(forms.ModelForm):
    class Meta:
        model = OrdemServicoItem
        fields = ["fase"]
