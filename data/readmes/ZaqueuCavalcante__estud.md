# Estud

[![Line coverage](https://zaqueucavalcante.github.io/estud/badge_linecoverage.svg)](https://zaqueucavalcante.github.io/estud)
[![Branch coverage](https://zaqueucavalcante.github.io/estud/badge_branchcoverage.svg)](https://zaqueucavalcante.github.io/estud)
[![Mutation score](https://zaqueucavalcante.github.io/estud/mutation/badge.svg)](https://zaqueucavalcante.github.io/estud/mutation)

O **Estud** é um sistema open-source para gestão educacional, utilizado por gestores, professores e alunos para descomplicar sua vida acadêmica.

Cadastre sua instituição de ensino em https://estud.com.br e comece a usar o **Estud** agora mesmo!

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/campus-dark.svg">
  <img alt="Tela de ocupação de campus do Estud: mapa de uso das salas por dia e turno, com indicadores de tempo usado e espaço alocado" src=".github/assets/campus-light.svg">
</picture>

### Gestor

- Organiza todas as turmas, salas e horários do semestre
- Entende o desempenho real dos alunos, tanto em frequência quanto em atividades/notas
- Controla a alocação de tempo e espaço do seu campus (geral, por turno e por sala)
- Cadastra cursos, grades curriculares, ofertas de curso e períodos de matrícula
- Notifica diretamente todos os usuários da sua instituição (recados, eventos, lembretes...)
- Define perfis de acesso customizados para sua operação, com permissões granulares
- Aumenta a segurança dos seus usuários através de Single Sign-On (SSO) e Two-Factor Authentication (2FA)
- Integra facilmente o Estud à outros sistemas via webhooks e eventos assíncronos

### Professor

- Organiza seu semestre, com agenda semanal e turmas ativas
- Monta o plano de aula diretamente no sistema, com suporte nativo a Markdown
- Realiza chamadas e publica atividades nas suas turmas
- Corrige as entregas, atribui notas e dá feedbacks direto aos seus alunos

### Aluno

- Acompanha com clareza sua jornada no curso, com dados de frequência e notas
- Organiza seu semestre, com agenda semanal, turmas atuais e atividades pendentes
- Recebe notificações sobre suas turmas, atividades e entregas (+ recados da instituição)
- Sabe em detalhes seu progresso atual e aproveitamento em cada turma
- Tira dúvidas com os professores a cada entrega realizada

## Tecnologias

O projeto utiliza diversas tecnologias e conceitos de design de sistemas:

- ASP.NET, Vue.js, Postgres
- RBAC, OAuth, SSO, 2FA, Multi-Tenant
- Workers, Outbox Pattern, Webhooks
- Cloudflare, Railway, Caddy, R2
- GitHub Actions, CI/CD Pipelines
- Unit, Integration, Mutation Tests
- OpenTelemetry, Grafana, PostHog
- Full Text Search, Audit Trail
- Vertical Slice Architecture

<picture>
  <source srcset=".github/assets/estud-arch.png">
  <img alt="Diagrama de arquitetura do Estud." src=".github/assets/estud-arch.png">
</picture>

## Qualidade e Testes

O sistema possui diversas funcionalidades e integrações com serviços externos, o que leva a uma grande quantidade de casos de uso que precisam ser validados continuamente conforme a evolução do projeto.

São +2.000 testes divididos entre unidade (30%) e integração (70%). Os de integração rodam contra dependências reais sempre que possível, pra testar o sistema do jeito que ele roda em produção:

- 𝗣𝗼𝘀𝘁𝗴𝗿𝗲𝗦𝗤𝗟 (banco com estrutura igual ao de produção)
- 𝗥𝘂𝘀𝘁𝗙𝗦 (possui a mesma API do Cloudflare R2 usado em produção)
- 𝗞𝗲𝘆𝗰𝗹𝗼𝗮𝗸 (IdP real, do mesmo tipo dos usados no SSO em produção)
- 𝗙𝗮𝗸𝗲𝘀 (servidor HTTP usado para simular Brevo, Google, IdP...)

Cada execução da suíte de testes gera +12k requests HTTP e +600k linhas lidas/escritas no banco de dados. Os altos índices de cobertura servem como quality gate para evitar que novas funcionalidades sejam introduzidas sem os devidos testes no projeto.

Todo commit na branch master ou PR aberto dispara um workflow no GitHub Actions, que roda os testes e gera relatórios de cobertura sobre a nova versão do código.

<picture>
  <source srcset=".github/assets/estud-tests.png">
  <img alt="Diagrama de testes do Estud." src=".github/assets/estud-tests.png">
</picture>

## Rodando localmente

Com o Docker instalado, basta rodar na raiz do repositório:

```bash
docker compose up --build
```

Isso sobe o Postgres (já com o schema criado), o backend em http://localhost:5000 e o frontend em http://localhost:3000.

Nesse modo as integrações externas ficam desligadas (login com Google, upload de arquivos no R2 e envio de e-mails pela Brevo). Os e-mails são escritos no log do backend — para fazer o primeiro acesso, crie sua conta pelo frontend e pegue o link de acesso com:

```bash
docker compose logs back | grep magic-link
```

Ao mudar o schema do banco, recrie o volume com `docker compose down -v`.
