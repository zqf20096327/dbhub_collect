# 🎧 HelpDesk Pro — Sistema de Gestão de Chamados de TI (ITSM)

<div align="center">

![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)
![Author: Dyego Assis](https://img.shields.io/badge/Author-Dyego%20Assis-blue.svg?logo=github)
![Node.js Version](https://img.shields.io/badge/Node.js-v20+-brightgreen.svg?logo=nodedotjs)
![Express](https://img.shields.io/badge/Express-4.19-lightgrey.svg?logo=express)
![React](https://img.shields.io/badge/React-19-blue.svg?logo=react)
![Vite](https://img.shields.io/badge/Vite-5.4-purple.svg?logo=vite)
![JWT](https://img.shields.io/badge/Auth-JWT-orange.svg?logo=jsonwebtokens)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker)
![Jest Tests](https://img.shields.io/badge/Tests-100%25%20Passing-success.svg?logo=jest)

**Sistema corporativo completo de suporte técnico e gerenciamento de incidentes de TI, desenvolvido com arquitetura moderna, conformidade de SLA, controle rigoroso de papéis (RBAC), auditoria de histórico, base de conhecimento e métricas em tempo real.**

[Demonstração Rápida](#-credenciais-de-acesso-para-testes) • [Arquitetura](#-arquitetura-do-projeto) • [Instalação Local](#-como-executar-o-projeto) • [Documentação da API](#-documentação-da-api-swagger--openapi) • [Docker Compose](#-executando-com-docker-compose)

</div>

---

## 📌 Visão Geral

O **HelpDesk Pro** foi concebido para atender às melhores práticas de gerenciamento de serviços de TI (ITSM / ITIL). A plataforma conecta solicitantes de diferentes departamentos da empresa aos analistas de suporte, permitindo triagem ágil, acompanhamento de prazos de SLA (Service Level Agreement), notas técnicas confidenciais, base de conhecimento para autoatendimento e avaliação de satisfação (CSAT).

---

## ✨ Funcionalidades Principais

### 👥 1. Perfis de Usuário e RBAC (Role-Based Access Control)
- **Solicitante:** Abre novos chamados, visualiza apenas suas solicitações, adiciona comentários, e ao final avalia o atendimento com notas e estrelas (CSAT).
- **Técnico / Analista de Suporte:** Acessa a fila global de chamados, assume tickets para sua fila ("Assumir Chamado"), atualiza status, registra notas técnicas internas (invisíveis ao solicitante) e publica artigos na Base de Conhecimento.
- **Administrador:** Acesso irrestrito a todas as áreas, gestão de usuários (promover/rebaixar papéis e ativar/desativar contas), controle do catálogo de categorias e visualização analítica completa de KPIs da equipe.

### ⏱️ 2. Acordo de Nível de Serviço (SLA) Dinâmico
- Cálculo automático do limite de atendimento conforme a criticidade:
  - **Urgente:** Prazo de **4 horas** úteis (alerta visual pulsante em caso de violação).
  - **Alta:** Prazo de **8 horas** úteis.
  - **Média:** Prazo de **24 horas** úteis.
  - **Baixa:** Prazo de **48 horas** úteis.
- Badges visuais inteligentes: `No Prazo` (verde), `Em Risco` (amarelo para prazos < 2h) e `SLA Violado` (vermelho).

### 🔄 3. Ciclo de Vida e Fluxo de Status
```
[Aberto] ➔ [Em andamento] ➔ [Aguardando usuário] ➔ [Resolvido] ➔ [Fechado]
                                                         │
                                                         └── (Reabertura pelo solicitante)
```

### 📜 4. Linha do Tempo e Auditoria Completa
- Toda ação é registrada em banco de dados (`ticket_history`): alteração de status, troca de prioridade, atribuição de técnico e fechamento, registrando o autor, valor anterior, novo valor e data/hora.

### 💬 5. Sistema de Comentários & Notas Técnicas
- Mensagens públicas trocadas entre usuário e analista.
- Suporte a **Notas Internas** (com ícone de cadeado e estilo dourado), permitindo que técnicos discutam soluções técnicas sem expor ao solicitante.

### 📧 6. Notificações por E-mail (Simulação em Tempo Real)
- Disparo automático de e-mails em eventos-chave: abertura de chamado, atribuição a técnico, alteração de status e novos comentários.
- Painel / Drawer visual e log no console simulando entrega SMTP em tempo real.

### 🌟 7. Avaliação de Atendimento (CSAT)
- Ao resolver o chamado, o solicitante pode atribuir de 1 a 5 estrelas e deixar um depoimento sobre o atendimento, alimentando o indicador CSAT da equipe no Dashboard.

### 📚 8. Base de Conhecimento (FAQ & Self-Service)
- Catálogo de artigos técnicos com busca instantânea.
- **Sugestão Inteligente:** Enquanto o usuário digita o título do chamado, o sistema busca e recomenda artigos da FAQ para que ele possa solucionar a dúvida sem precisar abrir o ticket!

### 📊 9. Dashboard Analítico & Métricas
- Indicadores de totalizadores de status.
- **MTTR (Mean Time to Resolution):** Tempo médio de atendimento em horas úteis.
- Taxa de conformidade e cumprimento de SLA.
- Gráfico de distribuição por categoria e nível de prioridade.
- Tabela de produtividade e média CSAT por técnico.

### 📥 10. Exportação de Relatórios em CSV
- Exportação com 1 clique de todos os chamados filtrados em formato CSV com UTF-8 BOM, pronto para abrir perfeitamente no Microsoft Excel, Google Sheets ou LibreOffice.

### 🎨 11. Design System & Modo Escuro / Claro
- Interface desenvolvida em Vanilla CSS moderno com suporte total a **Dark Mode** e **Light Mode**, efeitos de glassmorphism, micro-animações e tipografia profissional (Outfit & Plus Jakarta Sans).

---

## 🔑 Credenciais de Acesso para Testes

O banco de dados já vem populado com dados de exemplo (`npm run seed`). Você pode clicar nos botões de **Acesso Rápido** na tela de login ou utilizar as credenciais abaixo:

| Papel / Perfil | E-mail | Senha | Descrição de Acesso |
| :--- | :--- | :--- | :--- |
| **👑 Administrador** | `admin@helpdesk.com` | `admin123` | Acesso total: métricas, usuários, categorias e chamados |
| **🛠️ Técnico N2** | `tecnico@helpdesk.com` | `tecnico123` | Fila técnica, atribuição, notas internas e resolução |
| **👤 Solicitante** | `usuario@empresa.com` | `usuario123` | Abertura de chamados, comentários e avaliação CSAT |

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Node.js (v20+)** & **Express**
- **SQLite3** com wrapper Promise assíncrono (execução local zero-config)
- **JSON Web Token (JWT)** & **Bcryptjs** para autenticação e hash criptográfico
- **Swagger UI Express** & **OpenAPI 3.0** para documentação viva dos endpoints
- **Jest** & **Supertest** para testes automatizados de integração
- **CORS**, **Dotenv**

### Frontend
- **React (v19)** & **Vite (v5)**
- **Vanilla CSS Modular**: Design System com CSS Variables, Glassmorphism, temas claro/escuro
- **Lucide React**: Ícones semânticos de alta qualidade
- **Context API**: Gerenciamento de estado de Autenticação (`AuthContext`) e Tema (`ThemeContext`)

---

## 📁 Arquitetura do Projeto

```
helpdesk-pro/
├── backend/
│   ├── src/
│   │   ├── config/              # Conexão com banco de dados SQLite
│   │   ├── controllers/         # Regras de negócio (Auth, Tickets, Users, etc.)
│   │   ├── database/            # Schema DDL, migrations e seed rico
│   │   ├── docs/                # Especificação Swagger OpenAPI 3.0
│   │   ├── middlewares/         # JWT Auth, guardião RBAC e tratamento de erros
│   │   ├── routes/              # Rotas RESTful (/auth, /tickets, /dashboard, etc.)
│   │   ├── services/            # Serviços de SLA e simulador de e-mails
│   │   ├── app.js               # Configuração Express
│   │   └── server.js            # Inicialização e bootstrap assíncrono
│   ├── tests/                   # Testes automatizados Jest/Supertest
│   ├── Dockerfile
│   ├── .env.example
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── components/          # Sidebar, Navbar, Badges de SLA/Status, Modais
│   │   ├── contexts/            # AuthContext e ThemeContext (Dark/Light)
│   │   ├── pages/               # Dashboard, Tickets, Novo Chamado, KB, Admin
│   │   ├── services/            # Cliente HTTP com interceptor JWT
│   │   ├── styles/              # Design System em Vanilla CSS
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml           # Orquestração para deploy com 1 comando
├── LICENSE                      # Licença MIT
└── README.md                    # Documentação do projeto
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- [Node.js](https://nodejs.org/) v20 ou superior
- [Git](https://git-scm.com/)

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/helpdesk-pro.git
cd helpdesk-pro
```

### 2. Configurar e Executar o Backend
```bash
cd backend
npm install
npm run seed     # Popula usuários, categorias e chamados de demonstração
npm run dev      # Inicia o servidor backend na porta 5000
```
> O backend estará rodando em: `http://localhost:5000`  
> Documentação Swagger disponível em: `http://localhost:5000/api-docs`

### 3. Configurar e Executar o Frontend
Em outro terminal:
```bash
cd frontend
npm install
npm run dev      # Inicia o servidor Vite na porta 5173
```
> Acesse o sistema pelo navegador em: `http://localhost:5173`

---

## 🧪 Testes Automatizados

O backend possui suíte de testes de integração com **Jest** e **Supertest** cobrindo registro, login, ciclo de vida de tickets, transições de status e SLA.

Para executar os testes:
```bash
cd backend
npm test
```

---

## 📖 Documentação da API (Swagger / OpenAPI)

Com o backend em execução, acesse `http://localhost:5000/api-docs` para explorar e testar interativamente todos os endpoints da API:

| Método | Endpoint | Descrição | Permissão |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Cadastro de novo usuário | Público |
| `POST` | `/api/auth/login` | Autenticação e geração de JWT | Público |
| `GET` | `/api/auth/me` | Dados do usuário logado | Autenticado |
| `GET` | `/api/tickets` | Listagem de chamados com filtros e SLA | Autenticado |
| `POST` | `/api/tickets` | Abertura de novo chamado | Autenticado |
| `GET` | `/api/tickets/:id` | Detalhes, histórico e comentários | Autenticado |
| `PATCH`| `/api/tickets/:id` | Atualização de status e prioridade | Autenticado |
| `PATCH`| `/api/tickets/:id/assign` | Atribuição de analista responsável | Técnico / Admin |
| `POST` | `/api/tickets/:id/comments` | Inserção de comentário ou nota interna | Autenticado |
| `POST` | `/api/tickets/:id/rate` | Envio de avaliação CSAT e encerramento | Solicitante |
| `GET` | `/api/dashboard/metrics` | KPIs analíticos, MTTR e cumprimento de SLA | Autenticado |
| `GET` | `/api/categories` | Catálogo de categorias ativas | Autenticado |
| `POST` | `/api/categories` | Cadastro de categoria | Admin |
| `GET` | `/api/users` | Listagem de usuários | Admin |
| `PATCH`| `/api/users/:id` | Alteração de função (Role) e status | Admin |
| `GET` | `/api/knowledge-base` | Consulta a artigos da FAQ | Autenticado |
| `POST` | `/api/knowledge-base` | Publicação de novo artigo | Técnico / Admin |
| `GET` | `/api/export/tickets/csv` | Exportação de planilha em formato CSV | Autenticado |

---

## 🐳 Executando com Docker Compose

Para subir toda a aplicação em containers com apenas um comando:

```bash
docker-compose up --build
```

- **Frontend:** `http://localhost:3000`
- **Backend API:** `http://localhost:5000`
- **Swagger Docs:** `http://localhost:5000/api-docs`

---

## 📄 Direitos Autorais e Licença

Copyright © 2026 **Dyego Assis**. Todos os direitos reservados.

Este software é protegido pela legislação de direitos autorais e de propriedade intelectual (Leis nº 9.609/1998 e 9.610/1998). O uso, reprodução, modificação, distribuição, publicação, hospedagem ou execução depende de autorização prévia, expressa e por escrito do titular.

- **Desenvolvedor e Titular:** [Dyego Assis](https://github.com/dyegosan14-tech)
- **GitHub:** [https://github.com/dyegosan14-tech](https://github.com/dyegosan14-tech)
- **Contato para Solicitações de Uso:** [dyegosan14@gmail.com](mailto:dyegosan14@gmail.com)

Consulte o documento de termos completo em [LICENSE](LICENSE).

---

<div align="center">
Desenvolvido por <strong><a href="https://github.com/dyegosan14-tech">Dyego Assis</a></strong> com excelência técnica para portfólio profissional de alto nível.
</div>
