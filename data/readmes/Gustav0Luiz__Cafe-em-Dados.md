<div align="center">

# Café em Dados

<img
src="https://github.com/user-attachments/assets/27077935-d668-4cc0-9698-62394320af63"
alt="Café em Dados"
width="100%"
/>

<br>

Pipeline de dados end-to-end para integração e análise de dados públicos sobre a cadeia do café brasileiro.

<br>

[**Demo Dashboard**](https://gustav0luiz.github.io/cafe-em-dados-demo/) ·
[**Data Dictionary**](./dicionario.md)

</div>

---

## Overview

**Café em Dados** é um projeto de Engenharia de Dados que integra diferentes fontes públicas para construir uma visão analítica da cadeia do café no Brasil.

O pipeline reúne informações sobre:

* produtos e certificações de café;
* produção agrícola;
* exportações brasileiras;
* empresas e estabelecimentos da indústria do café.

Os dados são ingeridos e armazenados em **PostgreSQL**, transformados e testados com **dbt**, orquestrados pelo **Apache Airflow** e disponibilizados para análise em um dashboard via streamlit.

---

## Architecture

<img
align="center"
src="https://github.com/user-attachments/assets/40971289-258f-4d3d-86dd-2230ebc1069e"
alt="Café em Dados - Arquitetura"
width="100%"
/>



O pipeline segue uma arquitetura em camadas **Bronze → Silver → Gold**, separando ingestão, transformação e consumo analítico.

### Data layers

| Layer      | Purpose                                                                  |
| ---------- | ------------------------------------------------------------------------ |
| **Bronze** | Armazena os dados ingeridos das fontes externas com mínima transformação |
| **Silver** | Limpeza, tipagem, padronização e validação dos dados                     |
| **Gold**   | Modelos analíticos preparados para consumo pelo dashboard                |

As transformações **Bronze → Silver → Gold** são gerenciadas com **dbt**.

---

## Data Sources

| Source              | Data                        | Usage                                                        |
| ------------------- | --------------------------- | ------------------------------------------------------------ |
| **ABIC**            | Produtos certificados       | Qualidade, categorias, produtos e empresas                   |
| **IBGE / SIDRA**    | Produção Agrícola Municipal | Produção, área, produtividade e valor da produção            |
| **Comex Stat**      | Comércio exterior           | Exportações, produtos, destinos, estados e municípios        |
| **Receita Federal** | Dados Abertos do CNPJ       | Empresas e estabelecimentos relacionados à indústria do café |

Os dados de produção e comércio exterior utilizados no projeto abrangem o período de **2012 a 2024**.

Mais detalhes sobre cada fonte, seus campos e limitações estão disponíveis no [dicionário de dados](./dicionario.md).

---

## Tech Stack

| Component             | Technology              |
| --------------------- | ----------------------- |
| Ingestion             | Python                  |
| Large file processing | DuckDB                  |
| Data exploration      | Pandas                  |
| Database              | PostgreSQL              |
| Transformation        | dbt Core                |
| Data quality          | dbt tests               |
| Orchestration         | Apache Airflow          |
| Visualization         | Streamlit / Plotly      |
| Infrastructure        | Docker / Docker Compose |
| Version control       | Git / GitHub            |

---

## Pipeline

O Apache Airflow coordena as etapas de ingestão e transformação:

```text
Source check
     │
     ▼
  Ingestion
     │
     ▼
   Bronze
     │
     ▼
 dbt Silver
     │
     ▼
  dbt Gold
     │
     ▼
  Dashboard
```

A DAG principal é:

```text
cafe_em_dados_pipeline
```

O pipeline verifica quais fontes precisam ser atualizadas antes de executar cada ingestão.

Quando uma fonte não possui atualização necessária, sua etapa é marcada como `SKIPPED`, evitando processamento desnecessário das etapas dependentes.

O agendamento padrão da DAG é:

```text
06:00 — America/Sao_Paulo
```

---

## Data Processing

As fontes possuem características diferentes e exigem estratégias de processamento distintas.

### ABIC

Ingestão de dados públicos de produtos certificados e posterior padronização para análise de produtos, empresas e categorias.

### IBGE

Dados da **Produção Agrícola Municipal (PAM)** são obtidos através da API SIDRA e utilizados para análises por ano, estado, município e tipo de café.

### Comex Stat

Arquivos de comércio exterior são processados e filtrados pelos códigos NCM relacionados ao café antes da carga no banco.

### Receita Federal

A base pública do CNPJ possui grande volume de dados.

O **DuckDB** é utilizado para processar e filtrar os arquivos brutos antes da carga dos registros relacionados às atividades econômicas da cadeia industrial do café.

---

## Data Transformation

O **dbt Core** é responsável pela transformação dos dados armazenados no PostgreSQL.

```text
Bronze
   │
   ▼
Silver
   │
   ▼
Gold
```

Além das transformações SQL, o dbt é utilizado para:

* organizar dependências entre modelos;
* testar integridade e qualidade dos dados;
* validar valores e relacionamentos;
* manter a documentação técnica dos modelos.

Os modelos da camada Gold fornecem as tabelas utilizadas diretamente pelo dashboard.

---

## Dashboard

O resultado analítico do pipeline pode ser explorado em uma versão pública do dashboard:

### [Open Live Demo →](https://gustav0luiz.github.io/cafe-em-dados-demo/)

O dashboard está dividido em cinco áreas:

| Page           | Analysis                                               |
| -------------- | ------------------------------------------------------ |
| **Início**     | Indicadores gerais da cadeia do café                   |
| **Qualidade**  | Produtos e empresas certificados pela ABIC             |
| **Produção**   | Produção agrícola por estado, município e tipo de café |
| **Exportação** | Comércio exterior, destinos e produtos                 |
| **Indústria**  | Empresas e estabelecimentos relacionados ao café       |

> A versão publicada utiliza um snapshot estático dos modelos analíticos. O pipeline completo e automatizado está neste repositório.

---

## Project Structure

```text
Cafe-em-Dados/
│
├── dags/
│   └── cafe_em_dados_pipeline.py
│
├── dashboard/
│   ├── Home.py
│   ├── data/
│   ├── pages/
│   └── utils/
│
├── dbt/
│   ├── macros/
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
│
├── docker/
│   ├── dashboard/
│   └── postgres/
│
├── src/
│   ├── abic/
│   ├── comex/
│   ├── ibge/
│   └── receita/
│
├── .env.example
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── dicionario.md
└── README.md
```

---

## Quick Start

### Requirements

* Git
* Docker
* Docker Compose

Python, PostgreSQL, Airflow e dbt não precisam ser instalados localmente.

### 1. Clone the repository

```bash
git clone https://github.com/Gustav0Luiz/Cafe-em-Dados.git
cd Cafe-em-Dados
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Revise as variáveis do arquivo `.env` caso necessário.

### 3. Build the containers

```bash
docker compose build
```

### 4. Start the environment

```bash
docker compose up -d
```

Verifique os serviços:

```bash
docker compose ps
```

---

## Running the Pipeline

### Airflow

Acesse:

```text
http://localhost:8080
```

Localize a DAG:

```text
cafe_em_dados_pipeline
```

Na primeira execução, com o banco vazio, o pipeline constrói sequencialmente as camadas:

```text
Bronze → Silver → Gold
```

### Streamlit

Após a execução do pipeline, o dashboard local fica disponível em:

```text
http://localhost:8501
```

---

## Documentation

### Data Dictionary

O arquivo [`dicionario.md`](./dicionario.md) documenta:

* origem das fontes;
* significado dos dados;
* utilização no projeto;
* limitações;
* cuidados de interpretação.

### dbt

A documentação técnica dos modelos, colunas, dependências e testes é mantida junto ao projeto dbt.

---

## Author

**Gustavo Ribeiro**

[GitHub](https://github.com/Gustav0Luiz)

---

<div align="center">

**[Live Demo](https://gustav0luiz.github.io/cafe-em-dados-demo/)** ·
**[Demo Repository](https://github.com/Gustav0Luiz/cafe-em-dados-demo)**

</div>
