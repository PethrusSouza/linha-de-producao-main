# Sistema OS com Django

Este projeto agora tem uma camada Django para ligar o frontend ao backend e ao banco.

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

Login inicial:

```text
usuario: admin
senha: 123
```

Esse usuario agora usa a autenticacao oficial do Django, com senha criptografada na tabela `auth_user`.

## Banco de dados

O Django esta configurado para usar SQLite durante o desenvolvimento. Os dados ficam no arquivo:

```text
db.sqlite3
```

Os arquivos `.sql` ficam apenas como referencia da estrutura das tabelas. Os cadastros feitos pelo sistema sao gravados no `db.sqlite3`.

## Configuracao por ambiente

O projeto le variaveis do arquivo `.env` quando roda localmente. Use `.env.example` como modelo:

```text
SECRET_KEY=troque-essa-chave-em-producao
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
CSRF_TRUSTED_ORIGINS=https://seudominio.com,https://www.seudominio.com
DATABASE_URL=sqlite:///db.sqlite3
```

Em producao, essas mesmas variaveis devem ser cadastradas no painel da hospedagem. Para banco online, `DATABASE_URL` normalmente sera fornecida pela plataforma, por exemplo um PostgreSQL.

## Arquivos estaticos

O projeto usa WhiteNoise para servir CSS e arquivos estaticos em producao.

Antes de publicar ou quando alterar arquivos em `static/`, rode:

```bash
python manage.py collectstatic
```

Os arquivos coletados ficam em:

```text
staticfiles/
```

## Deploy

O projeto ja tem arquivos basicos para deploy:

```text
Procfile
runtime.txt
build.sh
```

Comando de build:

```bash
./build.sh
```

Comando de start:

```bash
gunicorn sistema_os.wsgi:application
```

Variaveis importantes para configurar na hospedagem:

```text
SECRET_KEY
DEBUG=False
ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS
DATABASE_URL
```

Para usar PostgreSQL online, configure `DATABASE_URL` com a URL fornecida pela hospedagem. O pacote `psycopg` ja esta no `requirements.txt`.

## Fluxo de ordens e producao

1. Cadastre clientes em `/clientes/`.
2. Cadastre itens/produtos em `/itens/`.
3. Crie uma ordem em `/dashboard/`.
4. Clique em `Abrir` na ordem criada para adicionar itens a ela.
5. Acompanhe as fases dos itens no painel `/painel-producao/`.

Cada item dentro de uma ordem pode estar em uma fase:

```text
Pre impressao
Impressao
Corte
Acabamento
Expedicao
Finalizado
```

Itens em `Finalizado` saem do painel de producao. O painel atualiza automaticamente a cada 10 segundos.

## Padroes de projeto usados

### MTV

O Django organiza o sistema com o padrao MTV:

```text
Model: producao/models.py
Template: templates/
View: producao/views.py
```

Os models representam as tabelas, os templates mostram as telas e as views controlam o fluxo entre formulario, banco e resposta ao usuario.

### Repository / DAO

O acesso ao banco foi centralizado em:

```text
producao/repositories.py
```

As views usam os repositories para buscar dados, por exemplo clientes, itens, usuarios e ordens recentes. Isso evita espalhar consultas como `Cliente.objects.all()` por varias partes do sistema.

## Autenticacao

O login usa o sistema oficial do Django:

```text
django.contrib.auth
```

Os usuarios novos cadastrados em `/usuarios/` sao gravados na tabela `auth_user`, com senha criptografada, e recebem um perfil em:

```text
perfis_usuarios
```

A tabela antiga `cad_usuarios` fica apenas como legado dos primeiros testes.
