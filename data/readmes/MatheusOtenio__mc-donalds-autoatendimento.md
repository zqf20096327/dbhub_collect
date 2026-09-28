[![English README](https://img.shields.io/badge/Language-English-blue?style=flat-square)](./README-EN.md)

# McDonald's Self-Service (Clone) - Autoatendimento

![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=flat-square&logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=flat-square&logo=tailwind-css)
![Prisma](https://img.shields.io/badge/Prisma-5-2D3748?style=flat-square&logo=prisma)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue?style=flat-square&logo=postgresql)
![Figma](https://img.shields.io/badge/Figma-Design-F24E1E?style=flat-square&logo=figma)

**Repositório:** [https://github.com/MatheusOtenio/mc-donalds-autoatendimento](https://github.com/MatheusOtenio/mc-donalds-autoatendimento)

---


## Sobre o Projeto

Este projeto é um sistema de autoatendimento completo para restaurantes, inspirado na experiência de usuário dos tótens do McDonald's e Burger King. A aplicação utiliza tecnologias modernas para recriar uma interface intuitiva, permitindo que clientes realizem pedidos de forma independente, visualizem o catálogo de produtos e gerenciem seu carrinho de compras com eficiência.

**Problema resolvido:** Redução de filas em estabelecimentos físicos, eliminação de erros de comunicação no pedido e modernização da experiência de compra do cliente através de uma interface visual e responsiva.

---

## Stack Tecnológica

### Frontend & Framework
- **Next.js** - Framework React para produção com renderização híbrida e otimizada
- **React** - Biblioteca para construção de interfaces reativas baseadas em componentes
- **TypeScript** - Superset do JavaScript com tipagem estática para maior segurança
- **Tailwind CSS** - Framework de estilização utilitário para design rápido e responsivo
- **Figma** - Ferramenta utilizada para prototipagem e design system

### Backend & Dados
- **Prisma** - ORM moderno para interação type-safe com o banco de dados
- **PostgreSQL** - Banco de dados relacional robusto
- **NeonDB** - Plataforma de banco de dados PostgreSQL serverless em nuvem

---

## Decisões Arquiteturais

### 1. Next.js para Performance e SEO

A escolha do Next.js permite uma arquitetura híbrida, otimizando o carregamento inicial das páginas (crucial para tótens de autoatendimento) e facilitando a renderização de conteúdo dinâmico do cardápio.

**Por que essa abordagem:**
- Melhor performance de carregamento (LCP) para o usuário final
- Roteamento simplificado baseado em arquivos
- Facilidade de deploy e escalabilidade na Vercel ou similares

### 2. Tipagem Estrita com TypeScript

Todo o projeto foi desenvolvido utilizando TypeScript para garantir a integridade dos dados desde o componente visual até a chamada ao banco de dados.

**Por que essa abordagem:**
- Redução drástica de bugs em tempo de execução
- Autocomplete e documentação do código através de tipos
- Manutenção facilitada à medida que o projeto cresce

### 3. Prisma como Camada de Dados

O Prisma atua como a ponte entre a aplicação Next.js e o banco de dados NeonDB, fornecendo uma API intuitiva e segura para manipulação de dados.

**Por que essa abordagem:**
- Type-safety end-to-end (do banco ao frontend)
- Migrations automatizadas para versionamento do schema
- Abstração da complexidade de queries SQL puras

---

## Funcionalidades Principais

**Navegação Visual**
- **Página Inicial:** Tela de boas-vindas convidativa para iniciar o fluxo.
- **Catálogo de Produtos:** Listagem categorizada com imagens de alta qualidade (Lanches, Bebidas, Sobremesas).

**Gestão de Pedidos**
- **Seleção de Itens:** Detalhamento do produto antes da adição.
- **Carrinho Dinâmico:** Revisão em tempo real dos itens selecionados, quantidades e valores.

**Experiência do Usuário (UX/UI)**
- Layout responsivo adaptável para tótens (telas grandes) e dispositivos móveis.
- Design System consistente inspirado em grandes players do mercado.

---

## Galeria do Projeto

| Página Inicial | Catálogo |
|:---:|:---:|
| ![Página Inicial](imagensRead/1.png) | ![Catálogo](imagensRead/2.png) |
| **Início do fluxo de pedido** | **Navegação por categorias** |

| Itens Selecionados | Carrinho |
|:---:|:---:|
| ![Itens Selecionados](imagensRead/3.png) | ![Carrinho](imagensRead/4.png) |
| **Detalhes do produto** | **Checkout e revisão** |

---

## Como Executar Localmente

### Pré-requisitos
- Node.js 18 ou superior
- Gerenciador de pacotes (npm, yarn ou pnpm)
- Conta no NeonDB (ou banco PostgreSQL local)

### Instalação

1. Clone o repositório
```bash
git clone [https://github.com/MatheusOtenio/mc-donalds-autoatendimento.git](https://github.com/MatheusOtenio/mc-donalds-autoatendimento.git)
cd mc-donalds-autoatendimento

```

2. Instale as dependências

```bash
npm install

```

3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto e adicione sua string de conexão:

```env
DATABASE_URL="postgresql://user:password@host:port/database?sslmode=require"

```

4. Execute as migrações do banco (opcional/se necessário)

```bash
npx prisma migrate dev

```

5. Inicie o servidor de desenvolvimento

```bash
npm run dev

```

O projeto estará disponível em `http://localhost:3000`

---


Desenvolvido por Matheus Otenio

Email: matheus.otenio843@gmail.com

```

```