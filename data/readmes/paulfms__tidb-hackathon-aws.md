# ✈️ CO²mpensa Aí — Compense a Emissão de Carbono com um clique

**Codinome:** GreenFlight
**Hackathon:** TiDB × AWS — São Paulo — 02/09/2026
**Time:** `latam-hackathon-007`

## 🌱 Sobre o projeto

O **CO²mpensa Aí** é uma solução criada durante o Hackathon TiDB × AWS com o objetivo de aproximar **tecnologia, experiência do passageiro e sustentabilidade** dentro do processo de compra de uma passagem aérea.

A proposta é permitir que o passageiro visualize, além do preço e das informações tradicionais do voo, a **estimativa de emissão de CO₂ por trecho** e tenha a possibilidade de compensar essa emissão diretamente durante o checkout.

A partir dessa compensação, o usuário recebe **Green Points**, enquanto a companhia aérea passa a ter acesso a indicadores relacionados à sustentabilidade e ao comportamento dos passageiros.

## 💡 Como funciona

Durante a busca por um voo, a aplicação apresenta informações como:

* ✈️ Origem e destino
* 💰 Preço da passagem
* 🕐 Horário e informações do voo
* 🌱 Estimativa de emissão de CO₂ por passageiro
* 🏷️ Classificação ambiental do voo

No checkout, o passageiro pode optar por compensar sua pegada de carbono.

A aplicação utiliza **busca vetorial e Inteligência Artificial** para encontrar e recomendar projetos de compensação alinhados às preferências informadas pelo usuário.

Após a confirmação, a compensação é convertida em **Green Points**, criando um mecanismo de incentivo para que o passageiro participe continuamente da iniciativa.

Para a companhia aérea, a solução disponibiliza indicadores ESG relacionados à adesão dos passageiros, CO₂ compensado, projetos apoiados e desempenho por rota.

## 🧠 Inteligência Artificial

A solução utiliza **Amazon Bedrock** para apoiar a recomendação e explicação dos projetos de compensação.

O **TiDB Vector Search** é utilizado para realizar a busca semântica dos projetos e conhecimentos relacionados à sustentabilidade, permitindo encontrar opções mais próximas da intenção descrita pelo passageiro.

## 🏗️ Arquitetura e tecnologias

* **Frontend:** React + Vite
* **Backend:** FastAPI
* **Banco de dados:** TiDB Cloud Starter
* **Busca vetorial:** TiDB Vector Search
* **IA:** Amazon Bedrock
* **Infraestrutura:** AWS EC2
* **Armazenamento:** Amazon S3
* **Desenvolvimento assistido por IA:** Kiro
* **Banco local / fallback:** SQLite

## 📁 Estrutura do projeto

```text
tidb-hackathon/
├── frontend/       # Interface da aplicação
├── backend/        # API e regras de negócio
├── sql/             # Scripts e estrutura do banco
├── docs/            # Documentação e arquitetura
├── scripts/         # Scripts de infraestrutura e deploy
└── .kiro/           # Specs, steering, hooks e MCP
```

## 👥 Participação

Este projeto foi desenvolvido de forma colaborativa durante o Hackathon TiDB × AWS.

A construção da solução envolveu momentos de **ideação, definição da proposta, desenvolvimento, integração das tecnologias, validação da solução e preparação da apresentação**, com participação conjunta dos integrantes do time.

### Integrantes

* **Paul Anderson**
* **Murilo Ribeiro**
* **Marco Luvizan**
* **Dorval Reis**
* **Moacir**

Cada integrante contribuiu para a evolução da solução de acordo com as necessidades do projeto e as diferentes etapas do hackathon.

## 🙏 Agradecimentos

Gostaria de deixar um agradecimento especial a **Murilo Ribeiro, Marco Luvizan, Dorval Reis e Moacir** pela parceria durante o hackathon.

Foi uma experiência muito positiva de colaboração, troca de ideias e construção conjunta. Em um projeto desenvolvido em um período tão curto, cada contribuição foi importante para transformar a ideia inicial em uma solução funcional.

**Obrigado, pessoal, pela parceria e pela construção do GreenFlight! 🚀🌱**

## 🤖 Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como ferramenta de apoio durante o desenvolvimento do projeto, auxiliando em etapas como exploração de ideias, geração e refinamento de código, documentação, resolução de problemas e prototipação.

A utilização dessas ferramentas fez parte da dinâmica de desenvolvimento do hackathon, enquanto as decisões sobre a solução, arquitetura, integração das tecnologias e direcionamento do produto foram realizadas pelo time.

## 🚀 Executando localmente

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
```

Em seguida:

```bash
cd ../frontend

npm ci
npm run build
```

Execute o backend:

```bash
cd ../backend

./.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em:

```text
http://localhost:8000
```

Com o `.env` sem configuração do TiDB, a aplicação pode utilizar o modo local com SQLite e o dump disponibilizado no projeto.

## 📚 Documentação

* [Documentação da plataforma](docs/PLATAFORMA.md)
* [Arquitetura do GreenFlight](docs/ARQUITETURA_GREENFLIGHT.md)
* [Documentação do banco e integração](sql/)
* [Submission do Hackathon](../SUBMISSION.md)

## 🔮 Próximos passos

Entre as possibilidades de evolução da solução:

* API pública de emissão de CO₂ por trecho;
* Integração com provedores certificados de créditos de carbono;
* Incentivos dinâmicos baseados em rota e ocupação;
* Personalização das recomendações para cada passageiro;
* Evolução do sistema de Green Points;
* Integração com motores de busca e plataformas de venda de passagens;
* Expansão dos indicadores ESG para companhias aéreas.

---

**CO²mpensa Aí / GreenFlight**
*Tecnologia para transformar cada viagem em uma escolha mais consciente. 🌎✈️*
