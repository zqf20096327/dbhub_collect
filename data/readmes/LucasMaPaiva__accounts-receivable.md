# accounts-receivable

[![CI](https://github.com/LucasMaPaiva/accounts-receivable/actions/workflows/ci.yml/badge.svg)](https://github.com/LucasMaPaiva/accounts-receivable/actions/workflows/ci.yml)

Microsserviço de contas a receber em Go, pensado como a extração de um módulo de um monólito Laravel.

O monólito (PHP) continua responsável pelo cadastro e pelas telas. Este serviço cuida dos títulos a receber: emissão,
pagamento parcial ou total, saldo e vencimento. A comunicação com o monólito é assíncrona, por fila, e o repositório
traz um monólito Laravel de exemplo em `exemplos/monolito-laravel` para mostrar os dois lados.

## Por que Go aqui

- Processo único e de longa duração: atende muitas requisições e consome fila ao mesmo tempo (goroutines), com pouca
  memória.
- Binário estático: a imagem Docker fica pequena e sobe em milissegundos.
- Tipagem estática e erros como valor de retorno: as regras de dinheiro ficam explícitas.

## Arquitetura

```
 monólito Laravel                                   accounts-receivable (Go)
 ────────────────                                   ────────────────────────
 vendas:faturar ─► job ──► [vendas] venda.faturada ──► contas.venda_faturada ──► worker ──► PostgreSQL
                                                  │ (inválida)                       │  titulos, pagamentos
                                                  └──► contas.venda_faturada.erro    │  eventos_processados
                                                                                     │  outbox
 HTTP (pagamento) ─────────────────────────────────────────────────────────► api ───┘
                                                                                     │
 consumidor ◄── monolito.titulo_pago ◄── [contas] titulo.pago ◄── relay da outbox ◄──┘
 (baixa na venda)
```

## Estrutura

```
cmd/api/              servidor HTTP com desligamento gracioso
cmd/worker/           consome venda.faturada e publica a outbox
cmd/mcp/              servidor MCP só leitura (stdio) para um assistente consultar os dados
cmd/simular-venda/    publica um venda.faturada como o monólito (desenvolvimento)
internal/eventos/     mensagens e processamento, sem depender do RabbitMQ
internal/mensageria/  topologia, consumidor e relay da outbox (amqp091-go)
migrations/           SQL versionado (golang-migrate), aplicado por um container antes da API subir
internal/titulo/      domínio: regras do título, sem HTTP nem banco
internal/repositorio/ onde os títulos ficam: Postgres (pgx) e memória, com os mesmos testes de contrato
internal/api/         handlers HTTP (net/http da biblioteca padrão)
internal/consulta/    consultas só leitura (saldo, vencidos, inadimplência) em pool READ ONLY
internal/metricas/    métricas Prometheus (HTTP, pagamentos, eventos, outbox)
internal/mcpserver/   ferramentas MCP sobre as consultas (SDK oficial go-sdk)
deploy/prometheus.yml coleta da API (:8080/metrics) e do worker (:9091/metrics)
.github/workflows/    CI: lint, testes com -race, integração com Postgres, PHPUnit e build das imagens
exemplos/monolito-laravel/   o outro lado: Laravel 13 que fatura vendas e recebe o titulo.pago
```

Dinheiro sempre em centavos (`int64`), nunca `float`.

## Rodar

Sem Go instalado, pelo Docker:

```sh
make test   # testes unitários com detector de condição de corrida
make test-integracao   # mesmos testes de contrato contra um Postgres real (banco contas_teste)
make up     # Postgres, migrations e API em http://localhost:8080 (imagem distroless)
make down   # para tudo (make reset apaga também o banco)
make psql   # console do banco (Postgres em 127.0.0.1:5444)
make venda  # publica um venda.faturada de teste (painel do RabbitMQ: http://localhost:15672, contas/contas)
make migration nome=criar_algo   # nova migration
make migrate-down / make migrate-up

make monolito-up   # tudo acima + monólito Laravel (fila e consumidor)
make faturar args="c1 15000"   # fatura uma venda no Laravel; o título aparece na API
make vendas        # vendas do monólito e se já foram pagas
make monolito-test # testes PHPUnit do monólito
make observar      # sobe também o Prometheus em http://localhost:9090
```

### Perguntar para o Claude

O `.mcp.json` da raiz registra o servidor MCP `contas-a-receber`. Abrindo o Claude Code nesta pasta (com o Postgres de
pé), dá para perguntar "quem está mais inadimplente?" ou "qual o saldo do cliente c2?". Ferramentas:

| Ferramenta | Responde |
|---|---|
| `saldo_cliente` | quanto o cliente deve, quanto já venceu e o próximo vencimento |
| `titulos_vencidos` | títulos vencidos com dias de atraso (todos ou de um cliente) |
| `inadimplencia` | clientes ordenados pelo valor vencido |

```sh
curl -X POST localhost:8080/titulos \
  -d '{"cliente_id":"c1","descricao":"Mensalidade","valor_centavos":10000,"vencimento":"2026-12-10"}'
curl -X POST localhost:8080/titulos/<id>/pagamentos -d '{"valor_centavos":4000}'
curl localhost:8080/titulos/<id>
curl "localhost:8080/titulos?cliente_id=c1&status=parcial&vencidos=true"
```

## Decisões

- **Pagamento em transação com `SELECT ... FOR UPDATE`.** Sem a trava, dois pagamentos simultâneos leem o mesmo saldo
  e um sobrescreve o outro (*lost update*). O teste `pagamentos simultâneos não estouram o saldo` dispara 10 pagamentos
  de 20,00 num título de 100,00: com a trava, 5 são aceitos e 5 recusados. Removendo o `FOR UPDATE`, os 10 são aceitos e
  o saldo fica errado (60,00 em vez de 0).
- **Regra no domínio e também no banco.** O domínio decide; os `CHECK` do Postgres garantem que nem um bug nem um
  `UPDATE` manual deixem pago acima do valor ou status incoerente.
- **`context.Context` em todo acesso ao banco.** Se o cliente cancela a requisição, a consulta é cancelada junto.
- **Mesmo contrato, duas implementações.** `testarContrato` roda igual na memória e no Postgres; o handler depende só
  da interface.
- **Idempotência no consumo (inbox).** A fila entrega "pelo menos uma vez". O `evento_id` é gravado em
  `eventos_processados` na mesma transação que cria o título; a mesma mensagem duas vezes cria um título só.
- **Erro permanente x temporário.** Mensagem inválida vai direto para a fila de erro (`Nack` sem requeue). Erro
  temporário (banco fora) volta para a fila; depois de 10 entregas (`x-delivery-limit` da fila quorum) também vai para
  a fila de erro, para não travar o consumo.
- **Outbox no `titulo.pago`.** Publicar no RabbitMQ dentro do handler cria o problema da escrita dupla: o banco grava e
  a fila falha (ou o contrário). O evento é gravado na tabela `outbox` na mesma transação do pagamento e um relay publica
  com *publisher confirms*, marcando como publicado só depois da confirmação. Testado com o RabbitMQ parado: o pagamento
  é aceito, o evento espera na outbox e sai quando a fila volta. `FOR UPDATE SKIP LOCKED` permite vários workers.
- **Do lado Laravel, a outbox sai de graça.** Com a fila `database`, o job `PublicarVendaFaturada` é gravado na tabela
  `jobs` na mesma transação da venda: ou os dois existem, ou nenhum. O job publica com *publisher confirms* e
  `mandatory` (mensagem sem fila vira erro); se o RabbitMQ estiver fora, o Laravel tenta de novo com espera crescente.
  Testado parando o RabbitMQ: 3 falhas (1 s, 5 s, 15 s de espera) e o título apareceu quando a fila voltou.
- **Id do evento estável.** O `evento_id` é `venda.faturada:<id da venda>`, não um aleatório: se o job rodar duas vezes,
  o serviço Go reconhece a repetição e não cria outro título.
- **Inbox também no Laravel.** O consumidor de `titulo.pago` grava o `message_id` (`outbox-<id>`, estável entre
  republicações do relay) em `mensagens_recebidas` na mesma transação da baixa. Testado republicando a mesma mensagem
  pelo painel: resultado `repetida`, venda intocada.
- **MCP só leitura em duas camadas.** As ferramentas são marcadas `readOnlyHint` e só fazem `SELECT`, mas a garantia
  real é do banco: o pool do MCP abre toda transação como `READ ONLY` (`default_transaction_read_only`). O teste de
  integração tenta um `UPDATE` por esse pool e confere o erro `25006` do Postgres. Em produção somaria um usuário só
  com `SELECT`.
- **Limite em toda lista do MCP.** O que a ferramenta devolve entra no contexto do modelo: `titulos_vencidos` tem teto
  de 500 e `inadimplencia` de 100, com padrão menor.
- **"Hoje" no fuso de Brasília.** Em UTC o dia vira às 21h; o servidor calcula a data em `America/Sao_Paulo` (fuso
  embutido no binário com `time/tzdata`) e o teste fixa 23h30 do dia 16 para conferir.
- **Métricas que respondem perguntas de negócio.** Além de requisições e latência, `contas_pagamentos_total`
  (aceito/recusado), `contas_eventos_consumidos_total` (criado/repetido/inválido/erro temporário) e
  `contas_outbox_pendentes`. Se a outbox só cresce, o relay parou: é o alerta mais útil do worker.
- **Rótulo com o padrão da rota, não o caminho.** `/titulos/{id}` em vez de `/titulos/abc123`: com o id no rótulo cada
  título viraria uma série nova no Prometheus. O teste chama três ids e confere que existe uma série só.
- **CI que roda o que roda local.** Lint (`gofmt`, `go vet`, `go mod tidy` sem diferença), testes com `-race`, testes
  de integração contra um Postgres de verdade (service container), PHPUnit do monólito e build das duas imagens.
- **Erro interno não vaza.** O detalhe vai para o log (JSON, `slog`) e o cliente recebe só "erro interno".

## Roteiro

- [x] Fase 1: domínio com testes e API HTTP com repositório em memória
- [x] Fase 2: PostgreSQL
  - [x] docker-compose com Postgres 17, healthcheck e migrations antes da API
  - [x] tabelas `titulos` e `pagamentos` com as regras também no banco (`CHECK` de valor, pago não excede o valor,
        status coerente com o pago; chave estrangeira no pagamento) e índices para listagem e vencidos
  - [x] repositório com pgx (pool) implementando a mesma interface do repositório em memória
  - [x] pagamento numa transação com `SELECT ... FOR UPDATE`, histórico em `pagamentos` e teste de concorrência
  - [x] listagem com filtros (cliente, status, vencidos) usando os índices
- [x] Fase 3: fila (RabbitMQ). O Laravel publica `venda.faturada`; um worker em Go consome, cria o título e publica
      `titulo.pago`. Idempotência pelo id da mensagem e reprocessamento com fila de erro
- [x] Fase 4: lado Laravel de exemplo (job que publica o evento e consumidor que dá baixa na venda). O título guarda a
      `venda_id` de origem e o `titulo.pago` a devolve
- [x] Fase 5: servidor MCP só leitura para consultar saldo, títulos vencidos e inadimplência por cliente
- [x] Fase 6: observabilidade (logs estruturados com slog, métricas Prometheus) e CI no GitHub Actions
