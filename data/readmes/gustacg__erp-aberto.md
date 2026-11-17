# ERP Aberto

ERP open source para pequenas e médias empresas brasileiras, construído em cima dos fluxos que essas empresas já usam no dia a dia: financeiro, vendas, compras, estoque, notas fiscais e cobrança.

![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-Postgres%20%2B%20Auth%20%2B%20Edge-3FCF8E?logo=supabase&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-celular-5A0FC8)

> **Publicado como está (*as is*).** Este é um projeto de desenvolvimento e estudo, aberto ao público. Não há suporte garantido nem desenvolvimento ativo. Pull requests são bem-vindos, mas podem não ser revisados. Antes de usar com dados reais, leia [Limitações](docs/LIMITACOES.md) e o [Aviso legal](#aviso-legal).

<!-- prints: docs/prints/inicio.png -->

## O que tem

| Módulo | O que inclui | Status |
|---|---|---|
| Cadastros | Clientes e fornecedores (uma pessoa, vários papéis; estrangeiro), produtos com variações, kits, conversão de unidade, categorias e marcas, serviços, listas auxiliares, consulta de CNPJ e CEP | ✅ Feito |
| Vendas | Orçamentos, aprovação que vira venda (baixa estoque e gera títulos), PDF do orçamento com link assinado, cópia de venda, contratos de venda recorrente | ✅ Feito |
| Frente de caixa (PDV) | Abertura e fechamento de caixa, pré-venda, sangria e suprimento, vendas por vendedor | ✅ Feito |
| Estoque | Situação, movimentações, movimento manual, inventário, histórico, estoque mínimo | ✅ Feito |
| Compras | Compras e cotações, compra recorrente, notas recebidas por manifestação (Focus NFe), entrada por XML, devolução ao fornecedor | ✅ Feito |
| Financeiro | Contas a receber e a pagar, baixas e estornos, parcelamento, categorias, centros de custo, contas financeiras, extrato com importação de OFX, fluxo de caixa, competência, DRE gerencial, inadimplentes | ✅ Feito |
| Relatórios e painel | Painel inicial, catálogo de relatórios, exportação CSV/XLSX, agendador de relatórios (arquivo gerado no sistema), pacote de XML e planilha para o contador | ✅ Feito |
| Usuários e perfis | Perfis de acesso (administrador, financeiro, vendas, comprador, contador; níveis júnior e sênior) com matriz de permissões, MFA por aplicativo opcional, troca de senha provisória | ✅ Feito |
| Auditoria e LGPD | Trilha de auditoria imutável, exportação de dados do titular, anonimização | ✅ Feito |
| PWA e push | Instala no celular pelo navegador, notificações Web Push | ✅ Feito |
| Importação de planilha | Clientes, fornecedores, produtos, serviços e saldo de estoque por CSV; títulos financeiros por planilha | ⚠️ Parcial (só CSV) |
| NF-e (Focus NFe) | Emissão, cancelamento, carta de correção, inutilização, devolução, nota de entrada, nota avulsa | ⚠️ Parcial: emissão real depende de certificado A1 e configuração na Focus NFe; regras fiscais precisam de validação de contador; ICMS-ST e IBS/CBS não são calculados |
| NFS-e (Focus NFe) | Emissão pelo padrão nacional | ⚠️ Parcial: padrão próprio de prefeituras não incluso |
| Cobrança (Asaas) | Boleto e Pix, webhook com baixa automática | ⚠️ Parcial: estorno parcial não reflete automaticamente em todos os casos |
| NFC-e / cupom fiscal | | ❌ Não incluso |
| E-mail transacional | Só o "esqueci a senha" do Supabase Auth | ❌ Não incluso |
| Maquininha / TEF | | ❌ Não incluso |

Detalhes do que está incompleto: [docs/LIMITACOES.md](docs/LIMITACOES.md).

<!-- prints: docs/prints/vendas.png -->
<!-- prints: docs/prints/financeiro.png -->
<!-- prints: docs/prints/celular.png -->

## Stack

| Camada | Tecnologia |
|---|---|
| Front | React 19, TypeScript, Vite 7, React Router 7, TanStack Query 5, react-hook-form + zod, Tailwind CSS 4, primitivos Radix, Recharts |
| PWA | vite-plugin-pwa (Workbox) e Web Push com VAPID |
| Banco | Supabase Postgres 17 com RLS em todas as tabelas, RPCs `SECURITY DEFINER` para escrita sensível, `pg_cron`, `pg_net`, Vault |
| Auth | Supabase Auth (e-mail e senha, MFA TOTP opcional) |
| Backend | Supabase Edge Functions (Deno) |
| Integrações | Focus NFe (notas fiscais), Asaas (boleto e Pix) |
| Qualidade | Biome, Vitest, Playwright, `deno test`, suítes SQL em `tests/db/` |

```
 navegador / PWA (React)
        │ supabase-js com chave publishable + sessão do usuário
        ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ Supabase                                                      │
 │  Auth · Postgres (RLS, RPC, triggers de auditoria, pg_cron)   │
 │  Storage privado · Vault (segredos)                           │
 │  Edge Functions: focus-*, asaas-*, push, exportar,            │
 │  orcamento-pdf, usuario-admin, importar-dados, ...            │
 └──────────────┬─────────────────────────┬──────────────────────┘
                ▼                         ▼
          Focus NFe (SEFAZ,         Asaas (boleto, Pix)
          prefeituras)
```

## Como rodar

### Pré-requisitos

- Node.js 20.19 ou mais recente (recomendado 22) e npm
- [Supabase CLI](https://supabase.com/docs/guides/cli)
- `psql` (cliente do PostgreSQL)
- [Deno](https://deno.com) (só para rodar os testes das edge functions)
- Opcional: conta na [Focus NFe](https://focusnfe.com.br) e no [Asaas](https://www.asaas.com)

### 1. Clonar

```bash
git clone <url-deste-repositorio> erp-aberto
cd erp-aberto
```

### 2. Criar o projeto Supabase

O Supabase é open source: use a nuvem ou instale você mesmo.

- **Nuvem:** crie um projeto em [supabase.com](https://supabase.com) (para dados no Brasil, região `sa-east-1`, São Paulo). Para produção, use um plano com cópia de segurança diária.
- **Self-hosted:** siga o [guia oficial com Docker](https://supabase.com/docs/guides/self-hosting/docker).
- **Local (desenvolvimento, Docker):** com Docker rodando e a Supabase CLI instalada, na raiz do repositório:

  ```bash
  supabase start -x edge-runtime   # usa supabase/config.toml; sem o -x o edge-runtime não sobe com as funções deste repo
  export DB_URL="postgresql://postgres:postgres@127.0.0.1:54322/postgres"
  supabase status                  # mostra API_URL, chaves e o Studio (http://127.0.0.1:54323)
  ```

  Nada disso fala com a nuvem: não rode `supabase link`. Para apagar tudo e começar de novo: `supabase stop --no-backup`.

No painel do Auth, desligue o cadastro público (só o administrador cria usuários) e defina a senha mínima em 10 caracteres.

### 3. Configurar o `.env`

```bash
cp .env.example .env
```

Preencha com os dados do seu projeto. Cada variável tem um comentário em [`.env.example`](.env.example). O `.env` nunca vai para o git.

### 4. Aplicar as migrations

As migrations ficam em `db/migrations/`, numeradas, e sobem do zero na ordem do nome (testado com o Supabase local, PostgreSQL 17).

`DB_URL` é a string de conexão do banco: no local, a do passo 2; na nuvem, a do painel (Connect, usuário `postgres`).

Antes da primeira migration, devolva ao `service_role` (o papel das edge functions) o acesso padrão às tabelas, sequências e funções novas do `public`. Projetos antigos da nuvem já vinham assim; o Supabase local e projetos novos não, e sem isso as edges e a fila recebem `permission denied`. As migrations tiram depois o que o `service_role` não deve ter (`0021`):

```bash
psql "$DB_URL" -X -v ON_ERROR_STOP=1 <<'SQL'
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT EXECUTE ON FUNCTIONS TO service_role;
SQL
```

Depois aplique todas, cada uma na sua transação e registrada em `public.schema_migrations` (como faz o `db/aplicar.sh`):

```bash
for f in db/migrations/*.sql; do
  v=$(basename "$f" .sql)
  { cat "$f"; echo; echo "INSERT INTO public.schema_migrations (versao) VALUES ('$v');"; } \
    | psql "$DB_URL" -X -q -1 -v ON_ERROR_STOP=1 || { echo "falhou em $v"; break; }
done
psql "$DB_URL" -XAtc "select count(*) from public.schema_migrations"   # deve dar o número de arquivos em db/migrations
```

Para as próximas, o script `db/aplicar.sh` aplica só as pendentes e tem modo de ensaio (`--ensaio`, em `BEGIN` e `ROLLBACK`). Ele foi feito para a nuvem (lê `SUPABASE_PROJECT_REF` e `SUPABASE_DB_PASSWORD` do `.env`, porta 5432 e SSL obrigatório) e não conecta no Supabase local; leia o cabeçalho dele antes de usar.

As provas SQL de `tests/db/` rodam com `db/aplicar.sh --teste arquivo.sql` ou, no local, com `{ echo 'BEGIN;'; cat arquivo.sql; echo 'ROLLBACK;'; } | psql "$DB_URL" -X -q -v ON_ERROR_STOP=1`. Muitas pressupõem a empresa configurada e usuários cadastrados (dados reais) e falham num banco vazio.

### 5. Gravar os segredos no Vault

Pelo SQL Editor do Supabase (os nomes e quem grava cada um estão em [docs/INTEGRACOES.md](docs/INTEGRACOES.md#supabase)):

```sql
select public.gravar_segredo('projeto_url', 'https://SEU-REF.supabase.co');
select public.gravar_segredo('fila_segredo', 'um-texto-aleatorio-longo');
select public.gravar_segredo('storage_chave_secreta', 'SUA-CHAVE-SECRET-OU-SERVICE-ROLE');
-- push (opcional): gere o par com supabase/functions/push/gerar_vapid.ts
select public.gravar_segredo('vapid_publica', '...');
select public.gravar_segredo('vapid_privada', '...');
select public.gravar_segredo('vapid_assunto', 'mailto:contato@seu-dominio.com.br');
-- Focus NFe (opcional)
select public.gravar_segredo('focus_token_master', '...');
```

No Supabase local, grave os três obrigatórios pelo `psql` (as chaves saem de `supabase status`; os valores só são usados quando a fila chama as edges):

```bash
psql "$DB_URL" -X -v ON_ERROR_STOP=1 <<'SQL'
select public.gravar_segredo('projeto_url', 'http://host.docker.internal:54321');
select public.gravar_segredo('fila_segredo', 'um-texto-aleatorio-longo-so-para-o-local');
select public.gravar_segredo('storage_chave_secreta', 'SECRET_KEY-DO-supabase-status');
SQL
```

### 6. Publicar as edge functions

```bash
supabase link --project-ref SEU-REF
supabase secrets set ORIGENS_PERMITIDAS=http://localhost:5173,https://seu-dominio.com.br
supabase functions deploy --project-ref SEU-REF
```

No self-hosted, as funções são copiadas para o volume de funções (veja o guia oficial). O `verify_jwt` de cada função está declarado em `supabase/config.toml`. O script `supabase/deploy.sh <função>` publica uma por vez e confere esse valor depois do deploy. `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY` e `SUPABASE_DB_URL` são injetados pelo Supabase em toda edge.

### 7. Criar o primeiro administrador

1. No painel do Supabase, em Authentication > Users, crie um usuário com e-mail e uma senha provisória. Copie o id (uuid).
2. No SQL Editor (só funciona enquanto não existe nenhum usuário no sistema):

```sql
select public.criar_usuario('UUID-DO-AUTH', 'Administrador', 'admin@seu-dominio.com.br', 'adm', null);
```

No primeiro acesso, o sistema pede a troca da senha provisória. Os demais usuários são criados pela tela.

### 8. Rodar o front

```bash
cd web
npm install
npm run dev
```

Abra `http://localhost:5173`. Outros comandos: `npm run build`, `npm run teste` (Vitest), `npm run lint` (Biome), `npm run e2e` (Playwright; credenciais de teste em [`web/playwright.config.ts`](web/playwright.config.ts)).

## Integrações

Detalhes técnicos em [docs/INTEGRACOES.md](docs/INTEGRACOES.md).

### Focus NFe (notas fiscais)

- **Chaves:** o Token Master fica no Vault (`focus_token_master`). Os tokens de produção e de teste da empresa são devolvidos pela Focus quando o administrador envia o certificado A1 em Configurações, e vão direto para o Vault. **Nenhuma chave fica no front.**
- **Certificado A1:** passa pela edge `focus-empresa` em memória e vai para a Focus. O sistema não guarda o arquivo nem a senha, só a validade e o CNPJ do certificado.
- **Webhooks:** a edge `focus-empresa` cria os gatilhos na Focus apontando para `focus-webhook`, que confere o cabeçalho `x-focus-segredo` antes de ler o corpo.
- **Emissão real** exige conta na Focus NFe, certificado A1 válido e a configuração fiscal (regime, CFOP, CST/CSOSN, alíquotas, série e numeração) validada por um contador.

### Asaas (boleto e Pix)

- **Chaves:** o administrador cola a chave de API do Asaas em Configurações > Asaas. A edge `asaas-cobranca` confere a chave, grava no Vault e cria o webhook. Nada de chave em variável de ambiente nem no front.
- **Webhooks:** `asaas-webhook` confere o cabeçalho `asaas-access-token` em tempo constante, enfileira o aviso e a fila consulta a cobrança no Asaas para aplicar o status (pago, estornado, cancelado).
- Juros e multa são configurados no painel do Asaas.

### Trocar de provedor

O resto do sistema fala com tabelas e RPCs próprias (`nota_fiscal`, `cobranca`, `titulo_financeiro`, fila `tarefa`). Para usar outro provedor, reescreva os arquivos que concentram a integração:

| Integração | Arquivos |
|---|---|
| Nota fiscal | `supabase/functions/_focus/` (cliente HTTP, URLs, montagem do JSON), `focus-empresa/`, `focus-nota/`, `focus-recebidas/`, `focus-webhook/` |
| Cobrança | `supabase/functions/asaas-cobranca/`, `supabase/functions/asaas-webhook/` |
| Push | `supabase/functions/push/` |

## Estrutura de pastas

```
.
├── db/
│   ├── migrations/      # SQL numerado: tabelas, RLS, RPCs, triggers, cron
│   ├── manual-ops/      # scripts manuais (limpeza de dados de teste, carga de demonstração)
│   └── aplicar.sh       # aplica migrations pendentes
├── docs/                # regras de negócio, modelo de dados, fluxos, integrações, LGPD, limitações
├── supabase/
│   ├── config.toml      # verify_jwt de cada edge function
│   ├── deploy.sh        # publica uma edge e confere o verify_jwt
│   └── functions/       # edge functions em Deno (_shared e _focus são código comum)
├── tests/db/            # suítes SQL rodadas em BEGIN/ROLLBACK
└── web/
    ├── src/
    │   ├── paginas/     # telas por módulo
    │   ├── componentes/ # componentes por módulo e da casca
    │   ├── api/         # cliente Supabase e chamadas
    │   └── sw.ts        # service worker (PWA e push)
    └── e2e/             # testes Playwright
```

Documentação funcional e técnica:

- [Regras de negócio](docs/REGRAS_DE_NEGOCIO.md)
- [Modelo de dados](docs/MODELO_DADOS.md)
- [Fluxos](docs/FLUXOS.md)
- [Integrações](docs/INTEGRACOES.md)
- [LGPD](docs/LGPD.md)
- [Armazenamento e retenção](docs/ARMAZENAMENTO.md)
- [Limitações conhecidas](docs/LIMITACOES.md)

## Segurança

- **RLS em todas as tabelas**, negando por padrão. Escrita sensível (baixa, cancelamento, emissão de nota, movimento de estoque) só por RPC `SECURITY DEFINER` ou edge function que confere a permissão. A tela esconde botões, mas quem trava é o banco.
- **Nada é apagado em silêncio:** venda, nota, título, baixa e movimento de estoque recusam `DELETE`; viram cancelados ou estornados, com registro na auditoria.
- **Segredos** de integração no Vault, nunca no front, em log ou no repositório. O `.env` está no `.gitignore`.
- **Webhooks** validam segredo no cabeçalho antes de ler o corpo e são idempotentes.
- **Storage privado** com links assinados.

Encontrou uma vulnerabilidade? Veja [SECURITY.md](SECURITY.md).

## Contribuindo

Veja [CONTRIBUTING.md](CONTRIBUTING.md).

## Aviso legal

- Projeto independente, sem vínculo com nenhuma empresa. As marcas citadas (Supabase, Focus NFe, Asaas e outras) pertencem aos seus donos.
- O software é fornecido **sem garantia de qualquer tipo**, conforme a [licença MIT](LICENSE).
- Regras fiscais, tributárias e de LGPD descritas aqui não são orientação contábil nem jurídica. **Valide com um contador** (e, para LGPD, com assessoria jurídica) antes de emitir notas ou tratar dados reais.

## Licença

[MIT](LICENSE) © ERP Aberto contributors
