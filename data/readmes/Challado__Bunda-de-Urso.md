# BUNDA DE URSO

O Bunda de Urso é um cadastro aberto de radares e outros equipamentos de
fiscalização eletrônica de trânsito no Brasil. Você pode buscar radares perto
de uma localização, consultar os detalhes e conferir a origem dos dados.

[Abrir o mapa](https://servidor3.lucas.inf.br/openclaw/radar/) · [API e exportação](docs/API_E_EXPORTACAO.md) · [Status das fontes](docs/STATUS.md) · [Histórico de alterações](CHANGELOG.md)

[Bundita de Urso](#bundita-de-urso) · [Traseiro de Urso](#traseiro-de-urso) · [Instalação e operação](#instalação-e-operação)

[![Validação](https://github.com/Challado/Bunda-de-Urso/actions/workflows/testes.yml/badge.svg)](https://github.com/Challado/Bunda-de-Urso/actions/workflows/testes.yml)

![Bunda de Urso — a bunda do urso com o radar tatuado](docs/bunda-de-urso.png)

> **O nome é uma provocação; o propósito é sério.**

> **🤖 Autoria:** este repositório — código, documentação e este README — foi **feito pelo Jarvis**, o assistente de IA (OpenClaw). Detalhes na seção [Autoria e proveniência](#autoria-e-proveniência), no fim.

## Uso da instância pública

O servidor público atende consultas individuais. Empresas, organizações e
operadores de aplicativos ou de outros sistemas devem usar uma instância
própria, inclusive em projetos sem fins lucrativos.
O arquivo diário está disponível para baixar a compilação com atribuição,
conforme a política de acesso.

Raspagem, cópia automatizada por paginação e redistribuição sem atribuição podem
levar à limitação ou ao bloqueio de acesso. Para conversar sobre acesso, use o
canal de contato. A compilação de dados continua sob CC BY 4.0, com atribuição
ao Bunda de Urso e respeito às condições das fontes originais.

[Política de uso](https://servidor3.lucas.inf.br/openclaw/radar/politica-de-uso.html) · [Arquivo diário](docs/API_E_EXPORTACAO.md#download-diário-da-base-pública) · [Contato](https://servidor.lucas.inf.br/site/contato) · [Licença dos dados](LICENSE-DATA.md)

## Bundita de Urso

O **Bundita de Urso** é o cadastro próprio de uma instalação. O operador
usa a API de escrita autenticada para incluir dados, como uma vistoria da
equipe em um ponto de fiscalização. O Radar guarda esses registros com
origem de cadastro próprio, no mesmo banco que armazena as coletas oficiais.

O formulário público também usa o nome Bundita de Urso. Ele recebe sugestões
em uma fila e devolve um protocolo. Após o processamento, os cadastros
aceitos entram como **colaborativos não verificados**, com fonte e histórico
próprios. No painel, a equipe pode revisar a contribuição e cruzá-la com
publicações oficiais. [Cadastrar radar](https://servidor3.lucas.inf.br/openclaw/radar/cadastro.html) · [Guia do Bundita](docs/BUNDITA_DE_URSO.md)

## Traseiro de Urso

O **Traseiro de Urso** é a rede opcional de troca de dados entre instalações.
Uma instância pode enviar e receber registros na mesma rodada, com token e
respeitando o intervalo e as paradas anunciados pelo outro servidor.
Os registros recebidos aguardam revisão em uma fila própria. Após aprovação
local, a posição pode ser publicada com a origem da rede preservada.

Por exemplo, uma instalação municipal pode oferecer seus pontos a outra
instalação. A equipe receptora confere as posições antes de publicá-las.
As instâncias também podem compartilhar instruções para ler fontes. Cada
instrução recebida começa desativada e só o administrador local pode ativá-la.
[Configurar o Traseiro](docs/TRASEIRO_DE_URSO.md) · [Protocolo para outros sistemas](docs/INTERCAMBIO_INSTANCIAS.md)

## Por que “Bunda de Urso”?

Bunda de Urso nasceu de um daqueles momentos em que a estrada te deixa na mão. Você vem no limite certo, confiando no navegador, no app de alerta, no radarzinho do painel — e, de repente, um flash. Ou pior: você passa por um equipamento que deveria estar ali, marcado, avisado, e não está. Nenhuma placa, nenhum aviso no aplicativo, nada. É aquela sensação de murchar por dentro, de “bunda flácida”, de ter sido deixado sozinho justamente pela informação que prometia te proteger.

E tem o outro lado, que dói igual: o radar que já morreu há anos, desligado, sucateado, arrancado do chão — e continua firme no mapa, como se estivesse lá. Aí você freia no vazio, por nada, todo dia no mesmo lugar, feito bobo.

A proposta é descobrir onde estão os equipamentos de fiscalização e
facilitar a conferência dos dados publicados. Cada cadastro pode reunir
localização, situação operacional e referências às fontes consultadas.

Não se trata de incentivar excesso de velocidade nem de escapar da fiscalização. Quem quer correr, que responda por isso. A ideia é aumentar a transparência, facilitar o respeito aos limites, reduzir informação incorreta e permitir auditoria pública de dados que, em tese, já são públicos.

## As lamúrias (ou: por que a gente ainda está aqui)

A lista é longa, e todo mundo que dirige tem a sua. A nossa está aqui embaixo:

- **O radar que não existe no mapa.** Está lá, na beira da pista, e o navegador jura que não há nada. O app de alerta, idem. Você só descobre na hora do flash.
- **O radar fantasma.** Desativado, removido, sucateado — e ainda marcado como ativo. Aí você freia por um poste vazio, todo dia, no mesmo lugar, feito palhaço.
- **A velocidade errada.** A placa (quando existe) diz uma coisa, o app diz outra, o cadastro diz uma terceira. Quarenta onde é sessenta, sessenta onde é quarenta. Ninguém sabe ao certo — e o bolso paga a conta.
- **O cadastro oficial sem coordenada.** O órgão publica, com orgulho, “KM 027+244M”. Ótimo. E onde fica isso, exatamente? A resposta, com sorte, é um trecho de 400 km de rodovia.
- **O dado espalhado em 27 portais.** Cada estado no seu formato: um em CSV, outro em PDF escaneado, outro numa página que só abre em navegador antigo, outro sem endereço nenhum.
- **A planilha sem cabeçalho e o PDF torto.** A fonte “oficial” chega sem coluna definida, com coordenada misturando grau decimal e grau/minuto/segundo — e, às vezes, com o sinal do oeste perdido no caminho.
- **A base comunitária decidindo se o radar existe.** Quando o órgão não publica, sobra o mapa colaborativo — que é útil, mas erra, e não deveria ser a única testemunha da existência de um equipamento.
- **O radar que aparece do nada.** Sem obra, sem aviso, atrás de uma placa, num trecho que ontem não tinha nada.
- **O órgão que publica a relação... de vez em quando.** Às vezes atualiza, às vezes esquece, às vezes tira do ar. E a multa continua chegando na sua casa.
- **O cidadão que só quer respeitar o limite.** Ele só quer saber qual é o limite, e o sistema inteiro parece fazer questão de esconder.

Ninguém aqui quer passar a mão na cabeça de quem corre. Queremos é que a informação deixe de ser favor, rumor ou PDF ilegível — e vire dado de verdade, com procedência e rastro.

## Missão

Construir um cadastro nacional independente de fornecedores comerciais, com foco em **latitude e longitude de cada equipamento**, complementadas por identificação física, órgão responsável, velocidade regulamentada, rodovia, quilômetro, sentido, faixas, tipo, datas, aferições e documentos de origem.

Ferramentas de navegação e projetos cartográficos podem usar uma instância
própria ou reutilizar a compilação publicada conforme a licença dos dados,
com atribuição ao Bunda de Urso e às fontes originais.

**Princípio essencial:** não inventar coordenadas, velocidades, situação operacional ou datas. Um registro sem posição exata permanece identificável e investigável, com localização candidata e grau de certeza explícitos.

## Cobertura pretendida

Todo o Brasil: União, 26 estados, Distrito Federal e municípios, em vias urbanas e rurais. Abrange controladores e redutores fixos, equipamentos portáteis, pontos autorizados de fiscalização, operações pontuais quando oficialmente publicadas e outros dispositivos de fiscalização eletrônica quando claramente identificados. Cada categoria deve ser diferenciada; uma câmera de monitoramento comum não é automaticamente um radar de velocidade.

A cobertura pretendida **não significa cobertura nacional completa já homologada**. O sistema deve declarar lacunas, fontes desatualizadas e áreas sem dados suficientes.

## Fontes de dados e política de confiabilidade

A fonte primária de existência, identidade, velocidade e situação de cada equipamento deve ser oficial: DNIT, PRF, ANTT, Inmetro/PSIE, DERs, Detrans, órgãos estaduais, concessionárias responsáveis por cadastros oficiais, órgãos municipais e portais governamentais de dados abertos.

Também são usados, para localizar geograficamente cadastros oficiais, dados cartográficos públicos como o Sistema Nacional de Viação (SNV/DNIT), sistemas rodoviários estaduais (SRE), serviços geográficos oficiais (ArcGIS REST, WFS, GeoJSON, KML e Shapefile) e o Cadastro Nacional de Endereços para Fins Estatísticos (CNEFE/IBGE).

OpenStreetMap não é fonte oficial para afirmar que um equipamento existe, está ativo ou fiscaliza certa velocidade. No módulo v1.4, o OSM pode ser consultado **somente como candidato auxiliar de localização**, quando já houver uma referência documental governamental, com revisão e identificação da proveniência. Waze e bases comerciais não alimentam automaticamente o cadastro oficial. Não são utilizados serviços pagos como dependência da coleta.

Os arquivos de origem são preservados com hash SHA-256, URL, data de coleta e, quando disponível, data de publicação. Registros conflitantes permanecem rastreáveis; o sistema não escolhe arbitrariamente um valor.

## Arquitetura

O projeto separa duas responsabilidades:

1. **Coletor e normalizador:** processo independente que descobre recursos oficiais, baixa documentos, interpreta formatos, valida campos, registra alterações e alimenta o banco relacional.
2. **Aplicação web/API:** interface de consulta que lê o banco local, sem consultar portais governamentais a cada requisição.

A API e os coletores usam Python 3. O banco pode ser SQLite ou PostgreSQL
com Psycopg 3 (`psycopg`). Algumas fontes exigem ferramentas auxiliares,
como Poppler para extrair tabelas de PDF. [Referência técnica](docs/README_TECNICO.md)

### Como a API é servida

No servidor3, o Nginx executa o programa Python `api.pse` sob demanda via
`fcgiwrap`. A extensão `.pse` segue a convenção local para scripts CGI.
O parâmetro `rota` indica qual operação atender.

```
https://servidor3.lucas.inf.br/openclaw/radar/api.pse?rota=/api/v1/radares&lat=-24.9555&lon=-53.4552&raio=5000&formato=json
```

O esquema relacional usa SQL e mantém versões para SQLite e PostgreSQL,
com as migrações em `sql/migracoes/`. SQLite é o padrão para instalações
novas. O migrador transfere o banco e o histórico e permite ativar
PostgreSQL para a API, os coletores e os crons. [Normalização relacional](docs/NORMALIZACAO_RELACIONAL.md) · [Migração para PostgreSQL](docs/MIGRACAO_POSTGRES.md)

## Como a coleta funciona

- Descobrir fontes e recursos oficiais cadastrados, inclusive catálogos CKAN e publicações geográficas.
- Baixar com limites de tamanho, timeout, tentativas progressivas, tratamento de 429/5xx, Retry-After, redirecionamentos e cache HTTP (ETag/Last-Modified/304).
- Preservar o arquivo bruto e registrar seu hash, metadados e histórico de tentativas.
- Ler CSV, JSON, XML, XLSX e formatos geográficos suportados; tratar formatos especiais por adaptadores específicos.
- Mapear os campos originais para entidades normalizadas sem descartar os valores brutos.
- Validar coordenadas, unidades, datas, limites de velocidade, identificadores e relacionamentos.
- Identificar possíveis duplicatas, preservando números de série, identificadores administrativos, faixas, sentidos e trocas de equipamento.
- Publicar apenas dados validados e manter o último lote íntegro quando uma atualização falhar.

Uma falha no portal de origem não deve derrubar a API. O cache e a base local continuam disponíveis, mas o sistema informa a idade dos dados e eventuais problemas de atualização.

A relação estadual da **AGETO/TO** também é coletada semanalmente, com GPS,
rodovia/km, série e número Inmetro. A carga pode usar o PDF local quando o
portal estiver indisponível. Veja [a fonte AGETO e os comandos pela API](docs/FONTE_AGETO_TO.md).

No painel de gestão, **Cruzamentos** confere novamente as contribuições ativas,
inclusive as já verificadas, com as fontes oficiais importadas. A tela de cada
contribuição também oferece **Cruzar com fontes oficiais**. As sugestões mostram
a fonte, a distância e divergências; a confirmação **Usar cadastro oficial** mantém
o ponto oficial no mapa e preserva o histórico da contribuição duplicada.
O cruzamento funciona sem IA. Veja [o fluxo e os endpoints](docs/CRUZAMENTOS.md).

## Assistência opcional

IA vem **desligada por padrão**. O painel administrativo oferece extração de documentos,
correspondências, auditoria, diagnóstico de coleta e explicações, sempre com alternativa
local e propostas para revisão. Aceita Ollama ou API externa compatível com OpenAI,
com chave cadastrada separadamente. O resumo público usa regras locais e fontes.
Veja [configuração, limites e funcionamento sem IA](docs/ASSISTENTE.md).

## O desafio central: onde diabos fica o radar

Nem todo cadastro governamental contém GPS. É o pecado original do setor: o órgão sabe que o radar existe, sabe a rodovia, sabe o quilômetro — e, mesmo assim, te deixa procurando um ponto no meio do nada. Por isso, Bunda de Urso possui um **resolvedor geográfico** que tenta localizar cada equipamento oficial:

**1. Coordenada oficial direta:** utilizar a latitude/longitude publicada pelo órgão, preservando a precisão declarada e o documento.

**2. Correspondência entre cadastros oficiais:** cruzar série, registro Inmetro, órgão, instalação, endereço, rodovia, quilômetro e período para aproveitar a coordenada presente em outra publicação do mesmo equipamento.

**3. Rodovia e quilômetro:** localizar um trecho georreferenciado oficial com referências quilométricas calibradas e calcular uma posição candidata sobre sua geometria. Não interpolar arbitrariamente sobre a extensão total da rodovia.

**4. Endereço:** buscar referência geográfica em cadastros oficiais municipais ou no CNEFE/IBGE. A coordenada de um endereço não é automaticamente a posição exata do poste do radar.

**5. Candidato comunitário opcional:** quando já existir identificação oficial suficiente, consultar OSM como pista de localização, nunca como comprovação autônoma da identidade ou da velocidade do radar.

**6. Revisão e pendência:** registrar candidatos, evidências, conflitos, aprovação ou rejeição e motivo. Se a localização exata não puder ser comprovada, conservar `latitude=null` e `longitude=null` ou uma posição estimada claramente marcada, sem fabricar exatidão.

A consulta por raio usa coordenadas em colunas numéricas comuns, filtragem por caixa delimitadora e distância geodésica por Haversine, sem exigir PostGIS. Para raios pequenos, como 10 m, a incerteza de uma coordenada derivada deve ser considerada explicitamente.

## Deduplicação e integridade

Dois registros próximos não são necessariamente o mesmo radar; duas faixas também não representam obrigatoriamente dois instrumentos físicos. A identidade é avaliada por série, fabricante/modelo, registro Inmetro, código administrativo, órgão, ponto, sentido, faixa e período de instalação.

- Duplicidade comprovada: unificar logicamente, mantendo todas as referências e o histórico.
- Equipamentos distintos: preservar registros separados, mesmo que estejam no mesmo ponto.
- Evidência insuficiente: gerar candidato para revisão, sem fusão silenciosa.
- Substituição de equipamento: registrar histórico temporal da instalação.

O banco usa chaves primárias e estrangeiras, restrições de integridade e relacionamentos normalizados. Não eliminar dados originais durante a consolidação.

A [normalização relacional e a identidade na escrita](docs/NORMALIZACAO_RELACIONAL.md)
foram revisadas: a atualização migra as relações redundantes e reconcilia
equipamentos comprovados, preservando fontes, histórico e IDs antigos.

O detalhe do radar e do equipamento faz a [junção da metrologia entre fontes oficiais](docs/JUNCAO_METROLOGICA.md)
pela série, tipo e município. Assim, uma instalação da GOINFRA pode mostrar o
histórico do Inmetro mesmo quando as duas publicações têm IDs de origem distintos.
As fontes e os valores divergentes continuam separados para conferência.
Quando a fonte não publica série, o detalhe também apresenta correspondência
cadastral por município, rodovia, km, sentido e velocidade, explicitando que a
identidade física ainda não foi confirmada. O instalador repara campos perdidos
lendo os brutos existentes, sem apagar ou recriar a base.
As [consultas de complementos](docs/CONSULTAS_E_COMPLEMENTOS.md) preferem
`LEFT JOIN`: ausência de endereço, documento, catálogo ou metadado não deve
eliminar o registro principal.

## Velocidades e fiscalização

O cadastro diferencia obrigatoriamente:

- Velocidade regulamentada geral, para veículos leves e para pesados.
- Limites específicos por faixa ou sentido, quando oficialmente publicados.
- Velocidade nominal do instrumento no Inmetro, que não equivale automaticamente ao limite da via.
- Velocidades observadas em estudos de tráfego, que não são limites regulamentados.

O tipo de equipamento (fixo, portátil), a função (controlador, redutor), o sentido, as faixas e a natureza da fiscalização (permanente ou pontual) são atributos distintos. Fiscalizações pontuais só recebem data/hora de início e fim quando isso constar de fonte verificável; não presumir operação ativa.

## API e formatos

A API consulta radares por localização, permite buscar cadastros por UF, município
ou rodovia e informa a origem de cada ponto. As consultas aceitam GET e POST.
Os formatos incluem JSON, NDJSON, XML, TXT delimitado, DIF e EDIFACT.
O arquivo diário `radares.json.gz` reúne a compilação pública.
[API e exportação](docs/API_E_EXPORTACAO.md) · [Ajuda da API](https://servidor3.lucas.inf.br/openclaw/radar/api.pse?rota=/api/v1/ajuda)

A consulta pode retornar zero pontos sem confirmar a cobertura da região.
Consulte `resultado.status` e `cobertura.completude_confirmada` para
interpretar o resultado. [Cobertura e erros](docs/API_E_EXPORTACAO.md#status-cobertura-e-erros)

## Governança da ingestão

Os controles seguem a origem do registro. A equipe usa a gestão para
verificar contribuições, revisar cruzamentos e corrigir ou remover
cadastros. Registros removidos saem das consultas e mantêm o histórico.
A API distingue a ingestão autenticada, a contribuição em fila e a troca
entre instâncias. [Guia de governança](docs/GOVERNANCA.md) · [Fila de cadastros](docs/FILA_CADASTROS.md) · [Cruzamentos](docs/CRUZAMENTOS.md)

## Atualizações, observabilidade e auditoria

No servidor3, a coleta, a fila, a rede e a geração do arquivo diário são agendadas no crontab do `www-data`. As fontes têm periodicidades próprias e a coleta reutiliza o cache persistente. [Configuração](docs/CONFIGURACAO.md)

A página de status mostra a cobertura por UF e as leituras oficiais. A equipe pode consultar as falhas detalhadas e os relatórios da instalação, da agenda e da fila. [Status](docs/STATUS.md) · [Relatórios de atualização](docs/RELATORIOS_ATUALIZACOES.md)

Os dados devem permitir rastrear cada resposta da API até a publicação original. Isso é indispensável para correção de erros e transparência pública.

## Instalação e operação

Os guias de configuração e instalação descrevem a operação atual. A
especificação v1.1 registra o desenho original do projeto.
[Referência técnica](docs/README_TECNICO.md) · [Especificação v1.1](ESPECIFICACAO_v1.1.txt)

Para testar em um checkout novo com SQLite:

```bash
cp -n deploy/radar.conf.exemplo radar.conf
mkdir -p dados
cp tests/fixtures/antt_radares_fixture.json dados/
python3 web/api.pse sync --fonte antt --arquivo "$PWD/dados/antt_radares_fixture.json"
```

O `radar.conf` fica na raiz do checkout ou, em produção, ao lado do
`api.pse` instalado. Para usar outro arquivo, indique o caminho com
`RADAR_CONF`. Na seção `[dados]`, a opção `dir` define onde ficam os
arquivos operacionais, e `motor` indica qual seção da configuração será
usada para o banco, `[postgres]` ou `[sqlite]`.

```bash
python3 web/api.pse configuracao mostrar
```

No servidor3, o instalador do repositório privado aplica as atualizações.
Em um servidor já preparado, execute este comando como root a partir da
pasta do instalador. Ele atualiza o código e o esquema e adia o reprocessamento.
[Guia de configuração](docs/CONFIGURACAO.md)

```sh
bash instalar-servidor3.sh --aplicar --sem-pacotes --sem-reprocessamento
```

O instalador também prepara o crontab do `www-data`. Se você ainda usa
o layout antigo, o guia explica como mover a instalação para a raiz web
preservando o banco existente. [Migração para a raiz web](docs/MIGRACAO_RAIZ_WEB.md)

Para rodar a suíte completa, incluindo os testes do instalador:

```bash
python3.13 .github/scripts/rodar_suite.py
```

O instalador requer Python 3.13 ou superior. O ambiente web usa Nginx,
fcgiwrap e um usuário com acesso ao banco configurado.

## Validação automática (CI)

Os testes de interface cobrem celular, tablet e PC nos três motores,
incluindo a gestão da rede. [Layouts e interações](docs/TESTES_LAYOUTS.md)

O workflow **Navegadores** testa o cadastro em Firefox e Chromium, com desktop
e tela estreita/toque, CGI e SQLite reais. Inclui rede indisponível, prazo de
resposta, reenvio e preservação do oficial. Veja [como executar e limites da
cobertura Android](docs/TESTES_NAVEGADOR.md).

Todo push no `main`, todo pull request e um disparo manual rodam a validação
rígida no GitHub Actions (`.github/workflows/testes.yml`). Nada passa por
"parece que está bom": cada checagem reprova o build.

**Suíte de testes** — Python 3.13, `compileall` de todo o código e a suíte
completa (`unittest`). O runner roda com piso de testes: se a coleta quebrar e
a suíte rodar "verde vazio", o job reprova.

**Rígido (contratos e invariantes)** — verificadores em `.github/scripts/`:

- **Paridade dos esquemas SQL** (`verificar_sql.py`): as tabelas e colunas dos
dois dialetos (`sqlite` × `postgres`) são as mesmas, e o DDL do SQLite executa
de verdade num banco em memória.
- **JSON** (`verificar_json.py`): todo JSON versionado parseia e não tem chave
repetida.
- **Segredos** (`verificar_segredos.py`): tokens do GitHub, AWS, Google, Slack
  e Telegram, chaves privadas e JWT; e arquivos que nunca podem entrar no git
  (`.env`, `config.php`, `*.pem`, `*.key`, credencial de conta de serviço).
- **Front** (`verificar_web.py`): todo `href`/`src` local existe, toda página
tem `viewport` (celular/tablet/PC) e as rotas que o front chama são atendidas
pela API (`web/nucleo.py`).
- **Escrita no banco** (`verificar_banco.py`): telas, console, cron e ferramentas
entram por `api.pse`; `tools/` contém clientes, sem isenção de acesso direto.
As operações locais de manutenção não são rotas HTTP. A única conexão física fica em
`core/db.py`.
- **Estrutura** (`verificar_estrutura.py`): arquivos obrigatórios presentes e
nenhum artefato de build/execução versionado (`__pycache__`, `.pyc`, bancos,
logs).

## Transparência e segurança viária

A Resolução CONTRAN nº 798/2020 prevê a publicidade da relação de medidores pelos órgãos responsáveis, incluindo a localização dos fixos, nos termos de seu art. 9º, parágrafo único. Isso não implica que cada órgão publique coordenadas GPS exatas, nem significa autorização irrestrita para qualquer uso de qualquer base de terceiros.

Fonte normativa: https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-contran/resolucoes/resolucao798-2020.pdf

O projeto apoia informação pública, fiscalização transparente, respeito aos limites e segurança viária. Alertas de navegação não substituem placas, regras de trânsito ou atenção do condutor.

## Visão de futuro

O objetivo é que uma consulta ao cadastro possa responder onde fica o
equipamento, qual velocidade fiscaliza, em que sentido, desde quando e
qual documento sustenta cada informação. Quando a origem não permite
confirmar um desses dados, a consulta deve indicar a lacuna.

No fim das contas, é isso: transformar a lamúria em dado. Para que ninguém mais freie no vazio, ninguém mais leve um flash por falta de aviso, e ninguém mais fique na mão por causa de informação que deveria ser pública e não é.

**Bunda de Urso: para que a informação sobre radares não deixe mais ninguém na mão.**

## Licença

O Bunda de Urso é **código-fonte disponível**, não software livre: o código está à vista, mas tem dono e regras de uso. Em resumo (o que vale é o texto do [`LICENSE`](LICENSE)):

| ✅ Pode | ❌ Não pode |
|---|---|
| instalar e usar para você, a sua família ou a sua organização | criar um projeto novo baseado neste código, no todo ou em parte, nem reescrito em outra linguagem |
| alterar o código da sua instalação | distribuir o código, original ou alterado, fora deste repositório |
| propor melhorias por pull request aqui | oferecer o sistema como serviço para outras pessoas |
| fazer fork no GitHub para preparar essas propostas | manter um fork como projeto separado |
| reutilizar os **dados** publicados sob CC BY 4.0 | apresentar os dados sem atribuição, ou como se fossem de outra origem |

Para qualquer outro uso, peça autorização pelo GitHub ([Challado](https://github.com/Challado)).

- **Dados:** o cadastro é compilado a partir de fontes oficiais públicas. A compilação e a estrutura são oferecidas sob **[CC BY 4.0](LICENSE-DATA.md)** (atribuição), respeitando os termos de cada fonte original.
- **Terceiros:** a pasta `referencia/` é material de terceiros e mantém a licença de origem.

## Autoria e proveniência

- **Contato:** [fale com o mantenedor](https://servidor.lucas.inf.br/site/contato).
- **Quem fez:** este repositório — o código, a documentação e este README — foi **escrito e mantido pelo Jarvis**, o assistente de IA (**OpenClaw**), a pedido do mantenedor do projeto. Os commits e os pushes também foram feitos pelo Jarvis.
- **Como foi feito:** em colaboração com o mantenedor, a partir da especificação do projeto e do material de referência.
- **O que não é nosso:** a pasta `referencia/` reúne material de referência de terceiros, guardado apenas para estudo e comparação; não é de autoria deste projeto nem do Jarvis.
