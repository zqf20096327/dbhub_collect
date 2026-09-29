# Doce Encanto Cupcakes — App de E-commerce

Aplicação web para uma loja virtual de cupcakes gourmet: vitrine de produtos, carrinho,
checkout, acompanhamento de pedidos e painel administrativo.

Projeto desenvolvido como parte do **Projeto Integrador Transdisciplinar em Engenharia de
Software II** — Cruzeiro do Sul Virtual.

## Stack técnico

- **Back-end:** Python 3 + Flask, padrão MVC (Model = SQLAlchemy, View = templates Jinja2,
  Controller = blueprints de rotas)
- **Banco de dados:** MySQL (produção) / SQLite (desenvolvimento local, automático)
- **Autenticação:** Flask-Login, senhas com hash (Werkzeug)
- **Front-end:** HTML + Bootstrap 5 (via CDN) + Jinja2
- **Testes:** Pytest (10 testes cobrindo cadastro, login, carrinho e controle de acesso admin)

## Estrutura do projeto (MVC)

```
cupcake_app/
├── app/
│   ├── __init__.py          # Factory da aplicação (cria e configura o Flask app)
│   ├── models.py            # MODEL — Cliente, Categoria, Produto, Pedido, ItemPedido
│   ├── routes/               # CONTROLLER — um blueprint por área
│   │   ├── main.py          # vitrine e detalhe de produto
│   │   ├── auth.py          # cadastro, login, logout
│   │   ├── cart.py          # carrinho, checkout, pedidos do cliente
│   │   └── admin.py         # CRUD de produtos e gestão de pedidos (admin)
│   ├── templates/            # VIEW — templates Jinja2
│   │   └── admin/
│   └── static/css/
├── tests/
│   └── test_app.py           # suíte de testes automatizados (pytest)
├── config.py                 # configuração (lê variáveis de ambiente)
├── run.py                    # ponto de entrada da aplicação
├── seed.py                   # popula o banco com categorias/produtos/admin de exemplo
├── schema.sql                # script DDL físico do banco (MySQL)
└── requirements.txt
```

## Como rodar localmente

```bash
# 1. Criar e ativar um ambiente virtual (opcional, mas recomendado)
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Popular o banco com dados de exemplo (usa SQLite por padrão, nenhuma configuração extra)
python seed.py

# 4. Rodar a aplicação
python run.py
```

Acesse **http://127.0.0.1:5000**.

**Login de administrador de exemplo (criado pelo seed.py):**
- E-mail: `admin@doceencanto.com`
- Senha: `admin12345`

## Rodando os testes

```bash
pytest tests/ -v
```

## Usando MySQL em vez de SQLite

Por padrão, a aplicação usa SQLite (arquivo local, zero configuração) para facilitar o
desenvolvimento. Para usar MySQL:

1. Crie o banco executando o script `schema.sql` no seu MySQL:
   ```bash
   mysql -u seu_usuario -p < schema.sql
   ```
2. Defina a variável de ambiente `DATABASE_URL` antes de rodar a aplicação:
   ```bash
   export DATABASE_URL="mysql+pymysql://usuario:senha@localhost/doce_encanto"
   python seed.py     # cria os dados iniciais no MySQL
   python run.py
   ```

## Deploy gratuito no PythonAnywhere (sugestão simples)

O [PythonAnywhere](https://www.pythonanywhere.com) oferece, no plano gratuito, hospedagem
para aplicações Flask **e** um banco de dados MySQL no mesmo painel — sem precisar configurar
dois serviços diferentes.

Passo a passo resumido:

1. Crie uma conta gratuita em pythonanywhere.com.
2. Na aba **Consoles**, abra um console Bash e clone o repositório:
   ```bash
   git clone <link-do-seu-repositorio-github>
   cd cupcake_app
   pip install --user -r requirements.txt
   ```
3. Na aba **Databases**, crie um banco MySQL gratuito (o painel já fornece host, usuário e senha).
4. Execute o `schema.sql` na aba **Databases** (console MySQL do próprio painel) para criar as tabelas.
5. Na aba **Web**, crie uma nova Web App, escolha "Manual configuration" + Python 3.10,
   e aponte o WSGI file para importar `run.app` (ajuste o caminho do projeto).
6. Configure a variável `DATABASE_URL` apontando para o MySQL criado no passo 3, no arquivo WSGI
   (antes do `from app import create_app`), ou usando um arquivo `.env`.
7. Rode `python seed.py` novamente no console para popular o MySQL de produção.
8. Clique em **Reload** na aba Web. A aplicação estará em `https://seuusuario.pythonanywhere.com`.

## Padrão MVC adotado

- **Model** (`app/models.py`): representa os dados e regras de negócio (ex.: `Produto.disponivel()`,
  `Cliente.checar_senha()`), isolado de HTTP e de apresentação.
- **View** (`app/templates/`): templates Jinja2 responsáveis apenas pela apresentação, sem lógica de negócio.
- **Controller** (`app/routes/`): recebe a requisição HTTP, aciona o Model, decide qual View renderizar.

## Rastreabilidade com as User Stories

Cada rota do sistema traz no docstring a referência à história de usuário que implementa
(ex.: `US01`, `US07`, `US17`), mantendo a rastreabilidade entre o backlog ágil e o código.
