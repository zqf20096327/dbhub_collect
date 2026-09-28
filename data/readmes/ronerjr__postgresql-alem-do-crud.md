# PostgreSQL Além do CRUD

> Um guia de decisão de arquitetura para quem usa PostgreSQL em produção — não é sobre sintaxe, é sobre trade-offs.

<p align="left">
  <a href="https://github.com/ronerjr/postgresql-alem-do-crud/releases/latest"><img src="https://img.shields.io/github/v/release/ronerjr/postgresql-alem-do-crud?style=for-the-badge&logo=github&color=blue" alt="Release v1.0" /></a>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-CC_BY--NC--SA_4.0-lightgrey.svg?style=for-the-badge" alt="CC BY-NC-SA 4.0" /></a>
  <a href="https://linkedin.com/in/ronerjr"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
</p>

`#postgresql` `#database-architecture` `#system-design` `#software-architecture` `#technical-guide`

---

## 🎯 Sobre o Guia

Este material discute decisões de arquitetura essenciais: modelagem de dados orientada ao domínio, escalabilidade, particionamento, replicação, observabilidade, migrações seguras e os trade-offs reais de operar PostgreSQL em produção em alta escala.

- 📄 **PDF completo no repositório:** [`docs/PostgreSQL_Alem_do_CRUD.pdf`](docs/PostgreSQL_Alem_do_CRUD.pdf)
- 🚀 **Download direto na Release:** [v1.0 - PostgreSQL Além do CRUD](https://github.com/ronerjr/postgresql-alem-do-crud/releases/tag/v1.0)

---

## 📚 Sumário do Guia

<details open>
<summary><strong>Expandir / Recolher Sumário Completo (32 Capítulos + Apêndices)</strong></summary>

### Parte 1 — Pensar PostgreSQL além das tabelas
- **1.** PostgreSQL não é apenas um banco relacional
- **2.** O modelo de dados é uma decisão de produto

### Parte 2 — Menos infraestrutura, mais inteligência
- **3.** Antes de adicionar Redis, veja se você realmente precisa dele
- **4.** Busca inteligente sem Elasticsearch
- **5.** SQL, NoSQL e vetor — mas não tudo ao mesmo tempo

### Parte 3 — Performance que não nasce de achismo
- **6.** O índice certo acelera; o errado cobra juros
- **7.** Pare de adivinhar: use EXPLAIN ANALYZE
- **8.** Dados grandes não exigem banco novo, exigem estratégia

### Parte 4 — Confiabilidade e segurança desde o início
- **9.** Concorrência é um problema invisível até quebrar produção
- **10.** Segurança não é apenas colocar senha no banco
- **11.** Backup que nunca foi restaurado não é backup

### Parte 5 — PostgreSQL preparado para o futuro
- **12.** Extensões que desbloqueiam novos produtos

### Parte 6 — O mapa de decisões de arquitetura
- **13.** Monólito modular vs. microserviços
- **14.** Banco compartilhado vs. banco por serviço
- **15.** Normalização vs. JSONB — matriz de decisão
- **16.** Cache local vs. UNLOGGED vs. Redis
- **17.** View vs. materialized view vs. tabela de leitura
- **18.** Trigger vs. lógica na aplicação vs. fila assíncrona
- **19.** Transação síncrona vs. processamento assíncrono
- **20.** Consistência forte vs. consistência eventual
- **21.** Particionamento vs. arquivamento vs. banco analítico
- **22.** Full-Text Search vs. Elasticsearch/OpenSearch
- **23.** RLS vs. filtro na aplicação vs. banco por tenant
- **24.** UUID vs. BIGSERIAL

### Parte 7 — Decisões que sobrevivem à produção e ao time
- **25.** Custo de reversibilidade: a pergunta antes de qualquer escolha
- **26.** Expand-contract: migrando sem downtime
- **27.** De sinal qualitativo a métrica: instrumentando o ponto de virada
- **28.** O que muda em ambiente gerenciado
- **29.** Custo é arquitetura: FinOps para decisões de banco
- **30.** Quem é dono desse schema? Governança e ADRs
- **31.** Testando antes de confiar: ambientes efêmeros e capacity planning
- **32.** Da decisão à RFC: como influenciar o time

### Conteúdo Complementar & Apêndices
- Checklist final — Antes de mudar a arquitetura
- Certificações e trilhas de evolução (PostgreSQL/EDB, Cloud e SRE/Plataforma)
- Matriz de evolução profissional e laboratórios recomendados

</details>

---

## 📋 Templates Práticos

O repositório inclui templates prontos para uso no dia a dia da sua equipe de engenharia:

- 🏛️ [ADR (Architecture Decision Record)](templates/adr-template.md)
- 📝 [RFC Técnico (Request for Comments)](templates/rfc-template.md)
- 🔄 [Checklist de Migração de Schema/Dados em Produção](templates/checklist-migration.md)
- ⚙️ [Checklist de Infraestrutura e Operação de Banco de Dados](templates/checklist-infra.md)

---

## ⚖️ Licença

Distribuído sob a licença [CC BY-NC-SA 4.0](LICENSE) (Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional).

---

## 👤 Autor

**Roner Damaso Junior** — Staff-level Software Engineer & Technical Architect. Atua profissionalmente com Tecnologia desde 2012, com experiência em sistemas distribuídos, arquitetura orientada a domínio e engenharia de dados em escala.

- 🌐 GitHub: [@ronerjr](https://github.com/ronerjr)
- 💼 LinkedIn: [linkedin.com/in/ronerjr](https://linkedin.com/in/ronerjr)

