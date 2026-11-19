# Doce Encanto Cupcakes — App de E-commerce

Aplicação web para uma loja virtual de cupcakes gourmet: vitrine de produtos, carrinho,
checkout, acompanhamento de pedidos e painel administrativo.

Projeto desenvolvido como parte do **Projeto Integrador Transdisciplinar em Engenharia de
Software II** — Cruzeiro do Sul Virtual.

- **Site publicado:** <https://doce-encanto-cupcakes.onrender.com> (o primeiro acesso pode levar ~1 min)
- **Documentação completa (S1, S2, S3):** [`docs/`](docs/README.md)
- **Manual de uso:** [`docs/S2-desenvolvimento/manual-de-uso.md`](docs/S2-desenvolvimento/manual-de-uso.md)
- **Vídeo 1 – Demonstração do sistema (narrado, 5:04):** <https://youtu.be/H0iX2982atU>
- **Vídeo 2 – Modificações após os testes (4:56):** <https://youtu.be/YTJZzke5LDA>

## Stack técnico

- **Back-end:** Python 3 + Flask, padrão MVC (Model = SQLAlchemy, View = templates Jinja2,
  Controller = blueprints de rotas)
- **Banco de dados:** TiDB Cloud, compatível com MySQL (produção) / SQLite (desenvolvimento local, automático)
- **Autenticação:** Flask-Login, senhas com hash (Werkzeug)
- **Segurança:** proteção CSRF (Flask-WTF), cookies HttpOnly/Secure, segredos em variáveis de ambiente
- **Front-end:** HTML + Bootstrap 5 (CDN) + Jinja2 + JavaScript
- **Testes:** pytest (back-end e HTML) + `node --test` (JavaScript): **119 testes**
- **Hospedagem:** Render (plano gratuito)

## Estrutura do projeto (MVC)

```
cupcake_app/
├── app/
│   ├── __init__.py          # Factory da aplicação, CSRF, filtros e páginas de erro
│   ├── models.py            # MODEL — Cliente, Categoria, Produto, Pedido, ItemPedido + regras de negócio
│   ├── routes/              # CONTROLLER — um blueprint por área
│   │   ├── main.py          # vitrine e detalhe de produto
│   │   ├── auth.py          # cadastro, login, logout
│   │   ├── cart.py          # carrinho, checkout, pedidos do cliente
│   │   └── admin.py         # CRUD de produtos e gestão de pedidos (admin)
│   ├── templates/           # VIEW — templates Jinja2
│   ├── static/              # CSS, JavaScript (checkout.js) e imagens
│   ├── formatacao.py        # filtros de exibição (R$ e horário de Brasília)
│   └── seguranca.py         # validação de redirecionamentos
├── certs/isrgrootx1.pem     # certificado PÚBLICO para o TLS do TiDB Cloud
├── docs/                    # documentação por situação-problema (S1, S2, S3) + roteiro do vídeo
├── tests/                   # testes automatizados (pytest) e tests/js (Node)
├── config.py                # configuração (lê variáveis de ambiente / .env)
├── run.py                   # ponto de entrada da aplicação
├── seed.py                  # popula o banco com categorias/produtos/admin de exemplo
├── verificar_banco.py       # diagnóstico SOMENTE LEITURA da conexão com o banco
├── definir_senha_admin.py   # troca a senha do administrador
├── schema.sql               # script DDL físico do banco (MySQL/TiDB)
├── .env.example             # modelo do arquivo .env (o .env real não vai para o Git)
└── requirements.txt
```

## Como rodar localmente (Windows / PowerShell)

```powershell
# 1. Criar o ambiente virtual e instalar as dependências
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. Criar o arquivo de configuração local
copy .env.example .env
#    (deixe DATABASE_URL vazio para usar SQLite; preencha SECRET_KEY)

# 3. Popular o banco com dados de exemplo
.venv\Scripts\python.exe seed.py

# 4. Rodar a aplicação
.venv\Scripts\python.exe run.py
```

Acesse **http://127.0.0.1:5000**.

**Administrador de exemplo (apenas no banco local):** `admin@doceencanto.com` / `admin12345`.
Essa senha é pública: **em produção, troque-a** (veja abaixo).

## Rodando os testes

```powershell
.venv\Scripts\python.exe -m pytest tests -v
```

Os testes usam um banco SQLite em memória: nunca alteram o banco local nem o TiDB.
Detalhes no [plano de testes](docs/S3-testes-e-validacao/01-plano-de-testes.md).

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `DATABASE_URL` | Em produção | `mysql+pymysql://USUARIO:SENHA@HOST:4000/doce_encanto`. Vazia = SQLite local |
| `SECRET_KEY` | Em produção | Chave aleatória do Flask. Gere com `python -c "import secrets; print(secrets.token_hex(32))"`. Sem ela, o app **não inicia** no Render |
| `DB_SSL_CA` | Não | Caminho de outro certificado CA (padrão: `certs/isrgrootx1.pem`) |
| `ADMIN_SENHA` | Não | Senha do admin criado pelo `seed.py` |

Localmente, coloque-as no arquivo `.env` (nunca envie esse arquivo para o GitHub).
No Render, cadastre-as em **Environment** no painel do serviço.

## Banco de dados TiDB Cloud

- O script físico está em [`schema.sql`](schema.sql). O dicionário de dados está em
  [`docs/S1-planejamento/05-dicionario-de-dados.md`](docs/S1-planejamento/05-dicionario-de-dados.md).
- A conexão usa TLS validado pelo certificado `certs/isrgrootx1.pem`.
- O TiDB vem com `tidb_enable_check_constraint` desligado (ignora `CHECK`). Por isso
  todas essas regras também são validadas na aplicação.
- Para conferir a conexão **sem alterar nada**: `python verificar_banco.py`.

## Trocar a senha do administrador

Com o `.env` apontando para o banco desejado:

```powershell
.venv\Scripts\python.exe definir_senha_admin.py
```

O script pede a nova senha duas vezes (ela não aparece enquanto você digita) e altera
somente a senha do usuário `admin@doceencanto.com`.

## Deploy no Render

1. Serviço **Web Service** ligado a este repositório (branch `main`).
2. **Build command:** `pip install -r requirements.txt`
3. **Start command:** `gunicorn run:app`
4. **Environment:** `DATABASE_URL` (TiDB Cloud) e `SECRET_KEY`.
5. Cada `git push` na `main` gera um novo deploy automaticamente.

## Padrão MVC adotado

- **Model** (`app/models.py`): dados e regras de negócio (ex.: `Produto.tem_estoque_para()`,
  `Pedido.cancelar()`, `Cliente.checar_senha()`), isolados de HTTP e de apresentação.
- **View** (`app/templates/`, `app/static/`): apresentação, sem regra de negócio.
- **Controller** (`app/routes/`): recebe a requisição, valida a entrada, aciona o Model e
  escolhe a View.

## Rastreabilidade com as User Stories

Cada rota traz no docstring a história de usuário que implementa (ex.: `US01`, `US07`,
`US17`). A matriz completa (história → código → teste) está em
[`docs/S1-planejamento/02-user-stories.md`](docs/S1-planejamento/02-user-stories.md).
