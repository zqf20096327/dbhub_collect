# 📊 Sistema de Controle de Gastos Residencial

Sistema web desenvolvido para **controle financeiro residencial**, permitindo o gerenciamento de **pessoas, receitas, despesas e saldos**, com foco em organização financeira, clareza das informações e boa experiência do usuário.

O projeto foi desenvolvido com **arquitetura moderna**, separação clara de responsabilidades e está **disponível em ambiente de produção**, sendo adequado tanto para uso real quanto para apresentação em **portfólio profissional**.

---

## 🔗 Acesso ao Projeto (Produção)

> ✅ **Aplicação em funcionamento**

- 🌐 **Front-end (Web)**:  
  👉 *[SCGR](https://scgr.vercel.app/)*

- 🔌 **API REST**:  
  👉 *[API](https://controlegastos-back.onrender.com/)*

- 📄 **Documentação da API (Swagger)**:  
  👉 *[Documentação](https://controlegastos-back.onrender.com/swagger/index.html)*

---

## 🧠 Visão Geral da Arquitetura

O sistema adota uma arquitetura **cliente-servidor**, com responsabilidades bem definidas:

- O **Front-end** é responsável pela interface, experiência do usuário e consumo da API.
- O **Back-end** concentra as regras de negócio, validações e persistência de dados.
- O **Banco de Dados** armazena as informações financeiras de forma estruturada e segura.

A comunicação entre as camadas ocorre via **HTTPS**, utilizando **JSON** como formato padrão de troca de dados.

---

## 🚀 Status do Projeto

- ✅ **Em Produção**
- 🔄 Deploy automatizado
- ☁️ Infraestrutura em nuvem
- 📈 Estrutura preparada para escalabilidade e evolução

---

## ⚙️ Tecnologias Utilizadas — Back-end

O Back-end foi desenvolvido em **.NET 8**, seguindo boas práticas de arquitetura, organização e manutenibilidade.

### 🔹 Linguagem e Plataforma

- **C#**
- **.NET 8**
- **ASP.NET Core Web API**

---

### 🔹 Arquitetura e Padrões

- **API RESTful**
- **DTO (Data Transfer Object)**
- **Injeção de Dependência**
- **Separação em Camadas**  
  *(Controllers, Services, Repositories)*

---

### 🔹 Persistência de Dados

- **Entity Framework Core**
- **TiDB Cloud (compatível com MySQL)**

O Entity Framework Core atua como ORM, facilitando o mapeamento objeto-relacional e o acesso aos dados, enquanto o TiDB Cloud garante alta disponibilidade e escalabilidade.

---

### 🔹 Outros Recursos

- **LINQ** para consultas
- **Swagger / OpenAPI** para documentação
- **Tratamento global de exceções**
- **CORS** configurado para comunicação segura com o Front-end

---

## 🎨 Tecnologias Utilizadas — Front-end

O Front-end foi desenvolvido como uma **Single Page Application (SPA)**, priorizando desempenho, organização do código e reutilização de componentes.

---

### 🔹 Linguagem e Framework

- **TypeScript**
- **React**

O TypeScript adiciona tipagem estática, aumentando a segurança e previsibilidade do código, enquanto o React facilita a construção de interfaces dinâmicas e reutilizáveis.

---

### 🔹 Gerenciamento de Estado e Lógica

- **React Hooks**
  - `useState`
  - `useEffect`
  - Hooks personalizados (`usePessoas`, `useLoading`, etc.)

Esses hooks permitem separar regras de negócio da camada de apresentação, promovendo maior organização e reutilização.

---

### 🔹 Comunicação com a API

- **Axios**

Utilizado para realizar requisições HTTP ao Back-end, com configuração centralizada da base da API.

---

### 🔹 Interface e Estilo

- **Bootstrap**
- **React-Bootstrap**
- **Lucide React (ícones)**

Essas ferramentas garantem um layout responsivo, consistente e agradável.

---

### 🔹 Feedback ao Usuário

- **React Toastify**

Utilizado para exibir mensagens de sucesso e erro, melhorando a experiência do usuário durante as operações do sistema.

---

### 🔹 Organização do Projeto

- **Components**: componentes reutilizáveis
- **Pages**: páginas principais
- **Hooks**: lógica reutilizável
- **Services**: comunicação com a API
- **Utils**: funções auxiliares (ex.: formatação de moeda)
- **Types**: tipagens TypeScript (DTOs)

---

## ☁️ Infraestrutura e Deploy

A aplicação utiliza uma infraestrutura moderna em nuvem, com serviços especializados para cada camada.

- **Front-end**:  
  Hospedado na **Vercel**, com deploy automático e CDN global.

- **Back-end**:  
  Hospedado na **Render**, executando a API REST em ASP.NET Core.

- **Banco de Dados**:  
  **TiDB Cloud**, banco distribuído compatível com MySQL.

---

## 🔐 Boas Práticas de Produção

- Uso de **variáveis de ambiente** para dados sensíveis
- Separação clara entre ambientes
- Código organizado e documentado
- Estrutura preparada para futuras evoluções:
  - Autenticação e autorização
  - Logs e monitoramento
  - Testes automatizados

---

## 📌 Considerações Finais

Este projeto demonstra a aplicação prática de conceitos fundamentais de **desenvolvimento web full stack**, **arquitetura em camadas**, **integração Front-end / Back-end** e **deploy em nuvem**, sendo ideal para apresentação em **portfólio profissional** ou como base para evolução futura.

---
