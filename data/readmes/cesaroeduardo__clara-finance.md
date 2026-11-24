<img width="2252" height="1168" alt="Frame 4" src="https://github.com/user-attachments/assets/e158cf5d-3b85-45d5-98d4-2fa4e670e001" />


# Clara Finance

**Clara Finance** (`clara-finance`) é um aplicativo de finanças pessoais, com um design refinado e um agente integrado, feito para você cuidar do seu dinheiro (como a Vó Clarinda sempre ensinou). Nele você acompanha receitas, despesas, contas bancárias conectadas via open-finance, faturas de cartão, investimentos e metas em um só lugar. Também permite registrar lançamentos manualmente, organizar categorias e regras de classificação, acompanhar recorrências e consultar os resultados por período.

O aplicativo roda no seu computador e armazena os dados em **SQLite local**. A integração com **Meu Pluggy** é opcional e importa contas, transações e investimentos autorizados por você. Também é possível testar a interface com dados fictícios, separados dos dados pessoais, sem configurar credenciais bancárias.

Construído com **Next.js 16, React, TypeScript, Tailwind CSS 4, shadcn/ui e Recharts**. Interface em português, valores em reais, datas no fuso America/Sao_Paulo e temas claro e escuro.

## Telas

<img width="1918" height="989" alt="image" src="https://github.com/user-attachments/assets/b1c57a40-12c5-44eb-b49b-1fe010096795" />

Visão geral com dados fictícios: gastos por categoria, investimentos e faturas dos cartões.

<img width="1917" height="938" alt="image" src="https://github.com/user-attachments/assets/adf1b693-03b3-4254-80bd-6cc6cc83053b" />

Metas com valores reservados, prazos e acompanhamento do progresso.

<img width="1919" height="988" alt="image" src="https://github.com/user-attachments/assets/2f4d6c1e-3056-4b36-9cc5-e57a5db01c3b" />

Agente com componentes agênticos.


## Começar

Requer Node.js 22.13+ e npm. O banco é criado automaticamente na primeira leitura. O pacote nativo `better-sqlite3` pode precisar de compilação: no Windows, Visual Studio Build Tools e Windows SDK 10.0.26100; no macOS, Xcode Command Line Tools.

### Windows (recomendado)

O script detecta o que falta (Node, Build Tools, Windows SDK), instala via winget se necessário (pode pedir administrador e demorar) e roda `npm ci`:

```powershell
git clone https://github.com/cesaroeduardo/clara-finance.git
cd clara-finance
.\setup-windows.cmd
npm run dev
```

### macOS (recomendado)

O script detecta Node e as Xcode Command Line Tools. Se faltar Node, instala via Homebrew; se faltarem as CLT, abre o instalador do sistema. Depois roda `npm ci`:

```bash
git clone https://github.com/cesaroeduardo/clara-finance.git
cd clara-finance
chmod +x ./setup-macos.sh
./setup-macos.sh
npm run dev
```

Se as Command Line Tools ainda estiverem instalando, conclua a janela do sistema e rode `./setup-macos.sh` de novo.

### Manual

Se Node e a toolchain nativa já estiverem ok:

```bash
git clone https://github.com/cesaroeduardo/clara-finance.git
cd clara-finance
npm ci
npm run dev
```

Abra http://127.0.0.1:3000. Para outra porta, use `npm run dev -- --port 3013`.

O aplicativo abre no espaço pessoal. Para testar com dados de exemplo, ative **Dados fictícios** na tela **Contas**. Desative o mesmo toggle para voltar aos seus dados. A escolha é lembrada no navegador. Os dois espaços ficam isolados no banco; a demonstração não sincroniza com a Pluggy.

Para usar a versão compilada:

```powershell
npm run build
npm start
```

O aplicativo inicia apenas na interface local (127.0.0.1). Ele foi feito para uma pessoa, em seu computador; não inclui login nem hospedagem pública.

### Atalho no desktop do Windows

Depois de instalar o Node.js e executar `npm ci` na pasta do projeto:

1. Abra a pasta do projeto no Explorador de Arquivos e localize `start-local.cmd`.
2. Clique com o botão direito no arquivo. No Windows 11, escolha **Mostrar mais opções**.
3. Selecione **Enviar para → Área de trabalho (criar atalho)**.
4. Na área de trabalho, renomeie o atalho para **Clara Finance**.
5. Para usar o ícone do projeto, abra **Propriedades → Atalho → Alterar ícone → Procurar** e selecione `public\clara.ico` dentro da pasta do projeto. Se o Windows avisar que o arquivo `.cmd` não contém ícones, confirme e escolha o arquivo `.ico`.

Ao abrir o atalho, uma janela de terminal inicia o servidor com `npm run dev`. Aguarde a mensagem de que o servidor está pronto e abra http://127.0.0.1:3000 no navegador. Mantenha o terminal aberto enquanto usa o aplicativo; para encerrar, pressione `Ctrl+C` nessa janela.

O atalho usa a localização atual de `start-local.cmd`. Se mover ou renomear a pasta do projeto, recrie o atalho. Ele não instala as dependências nem abre o navegador automaticamente.

### Acesso pela rede local (opcional)

Defina `ALLOW_LAN_ACCESS=true` em `.env.local` e reinicie com `npm run dev` ou `npm start` para acessar por outro dispositivo. O servidor passa a ouvir em `0.0.0.0`; acesse `http://IP-DO-COMPUTADOR:3000`. O `start-local.cmd` usa a mesma configuração. Com a variável ausente ou `false`, o acesso fica restrito ao computador.

O modo de rede continua **sem login**: qualquer dispositivo que alcance a porta pode ler e alterar seus dados. Use apenas em rede confiável, sem encaminhar a porta no roteador. Para webhook, use o túnel restrito descrito abaixo.

### Voz sintética (opcional)

O **modo voz** do agente funciona por padrão com o microfone e o `speechSynthesis` do navegador. A voz clonada via **Coqui XTTS** (sidecar Python local) é **opcional** e vem **desligada**.

Para ativar a voz sintética:

1. Prepare os áudios de referência e o sidecar (veja [`services/clara-xtts/README.md`](services/clara-xtts/README.md)).
2. Em `.env.local`:

```dotenv
NEXT_PUBLIC_CLARA_XTTS=true
CLARA_XTTS_URL=http://127.0.0.1:8020/tts
# opcional: sobe Next + XTTS no mesmo npm run dev
CLARA_XTTS_WITH_DEV=true
```

3. Reinicie o app. Com `CLARA_XTTS_WITH_DEV=true`, use `npm run dev`. Sem isso, rode o sidecar à parte (`services/clara-xtts/start.ps1`) ou `npm run dev:voice`.

Sem `NEXT_PUBLIC_CLARA_XTTS=true`, o modo voz não chama o XTTS. O modelo XTTS é pesado (~2 GB) e usa CPU/GPU local; na primeira execução pode demorar a baixar.

### Configurar o Logo.dev (opcional)

O Logo.dev fornece logos de instituições, estabelecimentos e algumas empresas exibidas no painel de mercado. O aplicativo funciona sem essa integração: o demo e o preview usam PNGs locais em `public/institutions`, `public/merchants` e `public/market` (regeneráveis com `scripts/download-demo-logos.mjs`). O símbolo do Sicredi continua sendo o arquivo oficial da marca.

1. Crie uma conta no [Logo.dev](https://www.logo.dev/) e abra [API keys no dashboard](https://www.logo.dev/dashboard/api-keys).
2. Copie a **Publishable key**, que começa com `pk_`. A **Secret key** (`sk_`) não é usada neste projeto.
3. Copie `.env.example` para `.env.local`, caso ainda não exista. Se já configurou a Pluggy, edite o arquivo existente e mantenha as outras variáveis.
4. Preencha a variável abaixo em `.env.local`:

```dotenv
NEXT_PUBLIC_LOGO_DEV_PUBLISHABLE_KEY=pk_sua_chave_publicavel
```

Reinicie `npm run dev`. Na versão compilada, execute `npm run build` novamente e depois `npm start`: variáveis `NEXT_PUBLIC_` são incorporadas ao código do navegador durante o build.

A chave publicável fica visível no navegador e nas URLs das imagens. Nunca coloque Client Secret da Pluggy ou uma chave `sk_` nessa variável. O código solicita imagens de `img.logo.dev` pelo domínio da marca; não envia valores ou descrições completas dos lançamentos ao Logo.dev.

Se ativar **Allowed domains only** no dashboard, cadastre os hosts usados para abrir o app, como `localhost` e `127.0.0.1`, sem protocolo, porta ou caminho. Para acesso pela rede, inclua também o host usado nesse acesso. Uma resposta `401` pode indicar chave incorreta ou host não permitido; `404` pode indicar logo indisponível. Consulte a [documentação de chaves e restrições](https://www.logo.dev/docs/platform/api-keys) e as [condições de atribuição do plano](https://www.logo.dev/docs/platform/attribution).

## O que funciona

- Dashboard com resultado mensal previsto, entradas, saídas, contas pendentes, fluxo acumulado, investimentos e metas.
- Lançamentos: criar, editar, excluir, pesquisar, filtrar por mês/categoria/tipo/situação e exportar CSV.
- Investimentos: posições manuais ou importadas, com instituição e classe.
- Metas: valor desejado, prazo, valor reservado e registro incremental de progresso.
- Contas: saldos e cartões importados, conexões e erros/estado da última sincronização.
- Tema claro/escuro, ocultação de valores e navegação responsiva.
- SQLite com WAL, migrações versionadas, chaves estrangeiras e valores inteiros em centavos.

## Conectar o Meu Pluggy (uso pessoal)

O caminho de uso pessoal é **Meu Pluggy + conector MeuPluggy**, conforme o [guia oficial](https://docs.pluggy.ai/pt/docs/guides/meu-pluggy-personal-use). Não use o conector bancário direto como substituto desse fluxo.

1. Entre em [meu.pluggy.ai](https://meu.pluggy.ai/) e autorize seus bancos.
2. Entre no [Dashboard Pluggy](https://dashboard.pluggy.ai/) com a mesma conta e crie/abra uma aplicação.
3. Na demonstração da aplicação, escolha **MeuPluggy** e autorize o acesso. Habilite o conector no grupo Pessoal se necessário.
4. Copie o **itemId de cada instituição** e as credenciais **Client ID** e **Client Secret**.
5. Copie `.env.example` para `.env.local` e preencha as credenciais:

```dotenv
PLUGGY_CLIENT_ID=seu_client_id
PLUGGY_CLIENT_SECRET=seu_client_secret
```

6. Reinicie o aplicativo. Na tela **Contas**, com **Dados fictícios** desativado, clique em **Adicionar conexão**, informe o nome e o itemId e depois clique em **Sincronizar**.

As credenciais e a API key ficam no servidor; o navegador recebe apenas o indicador de configuração. `.env.local`, banco, backups e arquivos de teste não são enviados ao Git.

A integração usa `/auth`, `/items/{id}`, `/accounts`, `/v2/transactions` e `/investments`. Ela não depende de listar todos os itens, recurso indisponível no uso pessoal. O fluxo de autorização permanece nos sites oficiais; não solicitamos a senha do banco dentro deste aplicativo.

### Comportamento da sincronização

- O botão lê os dados já disponíveis na Pluggy. Ele **não força uma atualização no banco**; o Meu Pluggy atualiza suas conexões a cada 24 horas.
- Importa todas as páginas e grava cada instituição de forma atômica. Erros não apagam os dados locais existentes.
- Reimportações atualizam pelo ID da Pluggy, sem duplicar transações. Categoria e tipo ajustados pelo usuário são preservados.
- Categorias e regras de classificação ficam no SQLite. As regras comparam a descrição do lançamento e definem a categoria. A categorização paga da Pluggy não é usada. Edições manuais e categorias já preenchidas são preservadas na reimportação; novos registros e os que estão `Sem categoria` recebem classificação automática.
- Pagamentos de fatura (`PAGAMENTO_FATURA`), aplicações e resgates financeiros (`APLICACAO_FINANCEIRA`, `RESGATE_APLIC_FINANCEIRA`, saldos reservados) e descrições típicas de aplicação/resgate/tesouro são classificados como transferência, para não entrar no resultado do mês. Rendimentos (`RENDIMENTO_APLIC_FINANCEIRA`) continuam como entrada. Confira PIX/TED para corretora e pagamentos de fatura sem identificador para evitar dupla contagem.
- Se investimentos não estiverem autorizados, a sincronização avisa e preserva as posições anteriores.
- A autorização pessoal expira após um ano. Renove no Dashboard/Meu Pluggy e confira os novos itemIds.
- O aplicativo limita o cadastro a cinco conexões pessoais, conforme o fluxo oficial.

### Webhooks opcionais

O receptor `POST /api/webhooks/pluggy` aceita `item/created`, `item/updated` e `item/error`. Ele grava o identificador do aviso no SQLite e responde `200 {"received":true}` antes de consultar a Pluggy. O processamento acontece com `after()` do Next.js. Apenas conexões pessoais já cadastradas na Clara são importadas; outros itens, aplicações e eventos são ignorados com `200`. O corpo do aviso não é usado como fonte de saldos ou mensagens de erro: o servidor lê o estado atual com sua própria API key.

Client ID e Client Secret continuam no `.env.local`, com os nomes `PLUGGY_CLIENT_ID` e `PLUGGY_CLIENT_SECRET`. Não copie esses valores para o código. Gere um segredo separado para autenticar os avisos:

```powershell
node --env-file-if-exists=.env.local scripts/pluggy-webhook.cjs setup
```

O comando adiciona `PLUGGY_WEBHOOK_SECRET` ao arquivo sem alterar as credenciais existentes nem imprimir o segredo. Reinicie o app e teste o receptor local:

```powershell
npm run dev
# Em outro terminal, na mesma pasta (substitua 3000 se usar outra porta):
node --env-file-if-exists=.env.local scripts/pluggy-webhook.cjs test 3000
```

O teste envia um item fictício não cadastrado. A resposta esperada é `200` com `received: true` e `ignored: true`; não consulta bancos e não comprova suas credenciais na Pluggy.

Para uma entrega real, a Pluggy exige HTTPS público. Com o [ngrok instalado e configurado](https://ngrok.com/docs/getting-started/), abra um túnel **limitado ao POST do webhook**, usando a política incluída. Ela bloqueia o dashboard e todas as outras rotas do aplicativo:

```powershell
ngrok http http://127.0.0.1:3000 --traffic-policy-file docs/pluggy-webhook-policy.yml
```

Cadastre a URL HTTPS mostrada pelo ngrok, acrescentando `/api/webhooks/pluggy`:

```powershell
node --env-file-if-exists=.env.local scripts/pluggy-webhook.cjs register https://SEU-DOMINIO.ngrok-free.app/api/webhooks/pluggy
```

Esse comando cria uma assinatura `all` na sua aplicação, com o cabeçalho `x-pluggy-webhook-secret`. Os cabeçalhos personalizados precisam ser cadastrados pela API, não pelo formulário do Dashboard. Execute uma vez por URL e remova a assinatura de teste no Dashboard ao terminar. Uma nova URL de túnel exige atualizar ou cadastrar o destino novamente.

Em [Eventos do Dashboard](https://dashboard.pluggy.ai/events), acompanhe uma nova entrega ou use **Retry** em uma entrega existente para esse destino. O app e o túnel precisam permanecer abertos. Um `401` indica segredo ausente/incorreto; `503`, configuração incompleta; `400`, JSON ou campos inválidos. Um `200` confirma o recebimento, e não a conclusão da importação. Veja o resultado da importação em **Contas & conexões** e atualize a página para exibir novos dados.

Avisos concluídos são deduplicados por `eventId`. Se o processamento falhar, a falha fica registrada e o mesmo evento pode ser reenviado. Avisos pendentes após um reinício são retomados na próxima entrega aceita. Não há um serviço de fila independente: se o computador for desligado depois do recebimento, reenvie pelo Dashboard; **Sincronizar** também recupera os dados diretamente. O recebimento de um `item/error` pode manter a conexão em erro até você renovar sua autorização no Meu Pluggy.

Referências: [webhooks da Pluggy](https://docs.pluggy.ai/en/docs/developer-tools/webhooks-ref), [cadastro pela API](https://docs.pluggy.ai/en/reference/webhooks) e [políticas do ngrok](https://ngrok.com/docs/gateway/traffic-policy/getting-started/agent-endpoints).

## Como os números são calculados

**Resultado previsto do mês = entradas − saídas**, incluindo registros pendentes. Transferências entre suas próprias contas não compõem esse resultado. Ele não equivale ao saldo bancário, que vem da instituição e aparece em Contas & conexões.

Os totais do dashboard e os gráficos consolidam BRL. Valores em outras moedas são mantidos e mostrados em sua moeda, sem conversão inventada. Investimentos representam posições atuais, não um histórico de rentabilidade. O campo `amount` da Pluggy é saldo bruto e não é tratado como custo de aquisição.

Os orçamentos são mensais. Metas representam o valor que você registrou como reservado: atualizar uma meta não transfere dinheiro, não cria um lançamento e não altera o saldo da instituição. Lançamentos manuais também não substituem o saldo importado.

## Categorias e regras de classificação

Em **Categorias**, os cartões identificam categorias padrão, personalizadas e a categoria protegida `Sem categoria`. Também mostram a quantidade de regras associadas. As categorias padrão podem ser renomeadas; as regras continuam vinculadas pelo ID. Apenas `Sem categoria` tem nome e exclusão protegidos.

No seletor da página, alterne entre **Categorias** e **Configuração**. A configuração mostra as regras em tabela, com busca e filtro por categoria. Ao editar uma categoria, o botão **Ver configurações** abre essa tabela já filtrada para ela.

Na tabela, use **Adicionar regra** ou o botão de edição da linha. Escolha se a descrição contém um texto ou é igual a ele, a categoria e a prioridade. A comparação ignora maiúsculas e acentos. O menor número de prioridade ganha; empates seguem a ordem de criação. Regras podem ser pausadas, editadas ou excluídas.

Alterações nas regras não reclassificam o histórico já preenchido. A sincronização mantém escolhas anteriores. Ao excluir uma categoria sem registros associados, suas regras também são excluídas.

Instalações novas recebem apenas regras genéricas de exemplo, gravadas uma vez no banco e editáveis pela interface. Regras pessoais não fazem parte desses dados iniciais. Na migração de uma instalação anterior, um arquivo local `<DATABASE_PATH>.legacy-category-rules.json`, se existente, é importado uma única vez. O arquivo contém uma lista de objetos com `match` e `category`; mantenha-o junto aos dados privados, fora do repositório. Depois da migração, o banco é a fonte das regras e o backup já as inclui.

## Proteção dos dados no Git

`npm ci` instala o hook de pre-commit em `.githooks`. Se houver outro `core.hooksPath`, ele é preservado: integre `node scripts/check-private-data.cjs` ao hook existente. Para reinstalar, execute `npm run prepare`.

O `.gitignore` exclui bancos SQLite e auxiliares, dumps SQL, backups, exportações CSV/OFX, arquivos de ambiente e logs. O hook inspeciona **o conteúdo em staging**, inclusive arquivos adicionados com `git add -f`, e bloqueia assinaturas SQLite, exportações reconhecidas e valores secretos locais. Também consulta nomes privados dos logos no banco local, quando disponível. `npm run security:check` verifica os arquivos atuais que seriam publicáveis; a CI repete essa verificação.

Logos pessoais e seus nomes ficam na tabela `merchant_assets`; as imagens são armazenadas no próprio SQLite e incluídas no backup. A migração opcional `<DATABASE_PATH>.legacy-merchants.json` importa uma lista `{ "match": "texto", "src": "data:image/png;base64,..." }` uma vez, apenas no modo pessoal. Novas instalações não recebem dados pessoais. Regras pessoais ficam em `category_rules`.

O banco e os backups não são criptografados pelo aplicativo. Mantenha-os em armazenamento protegido. Hooks podem ser ignorados e nenhuma detecção automática reconhece toda transcrição de dados: revise o diff antes de publicar. Essas proteções não apagam informações de commits antigos; o histórico precisa ser sanitizado antes de abrir o repositório.

## Banco e backup

O banco fica em `data/finances.sqlite`. Para mudar o local, defina `DATABASE_PATH` com um caminho absoluto em `.env.local`.

```powershell
npm run db:backup
```

O backup consistente é salvo em `data/backups/`. Para restaurar, feche o aplicativo, preserve o banco atual e seus arquivos auxiliares, e use o backup como o novo `finances.sqlite`. Não copie um banco em uso ignorando os arquivos WAL; use o comando de backup.

## Verificações

```powershell
npm test
npm run test:e2e
npm run typecheck
npm run lint
npm run build
```

Os testes cobrem persistência, validação, isolamento dos modos, centavos, moedas, transferências, metas, proteção de origem, importação paginada, reimportação, preservação de categorias e erros da Pluggy. Os testes de navegador usam Google Chrome instalado e um banco temporário em `work/`. Feche outro servidor `next dev` deste projeto antes de rodá-los.

A integração foi validada com respostas simuladas. A validação bancária real requer suas credenciais e itemIds.

## Referências visuais

O layout foi extraído visualmente da imagem fornecida: navegação lateral, fundo cinza claro, cartões brancos com cantos arredondados, azul nos controles, tipografia compacta e ilustrações 3D.

A coleção privada [Clara · Finanças pessoais no Mobbin](https://mobbin.com/collections/337bcdaf-33bd-49a7-81bb-73852b2b1b0a/mobile/screens) contém oito referências web selecionadas pelo MCP oficial. Ela é visível ao usuário e aos colegas com acesso no Mobbin. Consulte `docs/design-references.md` para os links e a função de cada referência.

Ilustrações locais da biblioteca [Thiings](https://www.thiings.co/things), convertidas para WebP e reduzidas para 320px (cerca de 210 KB no total). Os controles usam [shadcn/ui](https://ui.shadcn.com/) com Base UI e ícones Lucide.
