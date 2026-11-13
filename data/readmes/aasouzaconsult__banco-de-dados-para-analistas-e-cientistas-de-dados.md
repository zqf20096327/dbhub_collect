# Banco de Dados para Analistas e Cientistas de Dados

**Aprenda a consultar dados e transformar perguntas de negócio em análises com SQL.**

Este repositório reúne materiais de aula, e-books, scripts e um projeto prático de análise de vendas. O foco principal é SQL com MySQL, com materiais complementares de MongoDB, integração com R e Spark SQL.

O projeto **sales.z** simula uma demanda de consultoria: compreender uma base de vendas, construir consultas e documentar respostas para o cliente.

## Navegação

- [Para quem é este material](#para-quem-é-este-material)
- [O que você vai praticar](#o-que-você-vai-praticar)
- [Materiais do repositório](#materiais-do-repositório)
- [Como começar](#como-começar)
- [SQL: principais grupos de comandos](#sql-principais-grupos-de-comandos)
- [Projeto prático: análise de vendas da sales.z](#projeto-prático-análise-de-vendas-da-salesz)
- [Como documentar a entrega](#como-documentar-a-entrega)
- [Referências e ferramentas](#referências-e-ferramentas)
- [Sobre o autor](#sobre-o-autor)

## Para quem é este material

- Estudantes que estão começando a trabalhar com bancos de dados.
- Analistas que precisam consultar, relacionar e resumir dados para responder a demandas de negócio.
- Cientistas de dados que desejam fortalecer a etapa de obtenção e exploração dos dados.
- Professores e pessoas que buscam um caso prático para estudar SQL.

Conhecimentos básicos de tabelas, linhas e colunas ajudam no início. Os materiais de fundamentos podem ser usados como apoio durante os exercícios.

## O que você vai praticar

- Interpretar um modelo relacional e identificar como as tabelas se conectam.
- Selecionar, filtrar e ordenar registros.
- Relacionar dados com `JOIN`.
- Calcular contagens, somas, médias e outros indicadores.
- Trabalhar com textos, datas e expressões condicionais.
- Combinar resultados e criar views para organizar consultas.
- Enriquecer uma análise com uma fonte de dados complementar.
- Documentar o SQL, os resultados e as regras adotadas.

## Materiais do repositório

| Material | Conteúdo |
| --- | --- |
| [Fundamentos de SQL](Material%20da%20Aula/Fundamentos%20de%20SQL.pdf) | Material de aula em PDF. |
| [E-book SQL](Ebook%20-%20SQL/SQL.pdf) | Material de apoio para estudo da linguagem. |
| [SQL Ilustrado](Ebook%20-%20SQL/SQL%20Ilustrado.pdf) | Material complementar em PDF. |
| [Exemplos de SQL](scripts/1.%20SQL/SQL.sql) e [modelo](scripts/1.%20SQL/Modelo.png) | Script didático e modelagem da base de aula. |
| [Exemplos de NoSQL](scripts/2.%20noSQL/noSQL.txt) | Comandos e referências de MongoDB. |
| [Integração de R com MySQL](scripts/3.%20R/R.R) | Conexão, consultas e uso dos resultados em R. |
| [Integração de R com NoSQL](scripts/3.%20R/R_noSQL.R) | Exemplo complementar de integração. |
| [Spark SQL e PySpark](scripts/4.%20Spark%20SQL/) | Notebook de instalação do PySpark no Google Colab e arquivo de dados. |
| [Projeto sales.z](sales.z/) | Script de criação da base ERP, modelo relacional, dados complementares e exemplo de documentação. |

> A base dos exemplos de aula (`db_aula`) e a base do projeto (`ERP`) são diferentes. Use o script correspondente à atividade que estiver realizando.

## Como começar

### 1. Prepare o ambiente

Para o projeto principal, utilize uma instalação do [MySQL](https://dev.mysql.com/downloads/mysql/) e um cliente SQL, como o [MySQL Workbench](https://dev.mysql.com/downloads/workbench/).

MongoDB, R e PySpark são necessários apenas para os respectivos materiais complementares.

### 2. Conheça a base do projeto

Abra o [modelo relacional da sales.z](sales.z/1.%20Modelagem_BD_ERP.png) e consulte o [script de criação e carga](sales.z/1.%20Script_Criacao_BD_ERP.sql).

O script cria o banco `ERP` e tabelas de vendas, vendedores, dependentes e estoque de produtos. As vendas também contêm informações de clientes, produtos e canais de venda.

### 3. Crie a base em um ambiente de estudo

Baixe o script, abra-o no cliente SQL, revise os comandos e execute a criação das tabelas e a carga dos dados em uma instância de estudo.

O script usa variações de maiúsculas e minúsculas nos nomes das tabelas. Se o seu ambiente diferenciar esses nomes, padronize as referências antes de executá-lo.

Após a carga, selecione a base e confira as tabelas:

```sql
USE ERP;
SHOW TABLES;
```

### 4. Resolva as perguntas e documente as respostas

Comece pela Fase 1 e avance para a Fase 2. Para cada questão, registre a consulta, o resultado e uma breve interpretação.

Consulte os exemplos de aula quando precisar revisar um comando. Para os materiais em R, ajuste os parâmetros de conexão ao seu ambiente.

## SQL: principais grupos de comandos

SQL (*Structured Query Language*) permite definir estruturas, consultar e manipular dados, controlar acessos e gerenciar transações.

| Grupo | Finalidade | Exemplos |
| --- | --- | --- |
| **DDL — Data Definition Language** | Definir e alterar estruturas. | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML — Data Manipulation Language** | Inserir, atualizar e excluir registros. | `INSERT`, `UPDATE`, `DELETE` |
| **DQL — Data Query Language** | Consultar dados — foco principal do projeto. | `SELECT` |
| **DCL — Data Control Language** | Controlar permissões de acesso. | `GRANT`, `REVOKE` |
| **TCL — Transaction Control Language** | Controlar transações. | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

A classificação pode variar entre referências: algumas incluem `SELECT` em DML. A sintaxe e os recursos disponíveis também dependem do sistema de banco de dados utilizado.

## Projeto prático: análise de vendas da sales.z

### Contexto

Você faz parte da **data.z — consultoria em dados**. A empresa fictícia **sales.z** contratou sua equipe para analisar os dados de vendas e apoiar um estudo sobre clientes, produtos, vendedores e canais.

O cliente disponibilizou uma base de amostra com dados fictícios, estruturada para representar um cenário de ERP.

### Arquivos do projeto

- [Modelo relacional](sales.z/1.%20Modelagem_BD_ERP.png).
- [Script de criação e carga da base ERP](sales.z/1.%20Script_Criacao_BD_ERP.sql).
- [Dados de escolas — Censo Escolar 2020/INEP](sales.z/Censo2020_inep.csv).
- [Exemplo de documentação da entrega](sales.z/modelo_doc.md).

![Modelo relacional da base ERP utilizada no projeto sales.z](sales.z/1.%20Modelagem_BD_ERP.png)

### Orientações

- Elabore uma consulta por questão.
- Preserve os registros e a estrutura das tabelas durante a análise. A criação de views faz parte dos exercícios que a solicitam.
- Respeite os filtros de vendas concluídas e não deletadas quando indicados.
- Confira os valores existentes na base antes de definir filtros de status, sexo, canal ou exclusão lógica.
- Quando uma pergunta admitir mais de uma interpretação, documente a regra utilizada.
- Para o enriquecimento com dados do INEP, importe o CSV para uma tabela auxiliar no ambiente de estudo, preservando os dados originais do ERP.
- Em uma atividade orientada, alinhe dúvidas de negócio com o professor ou responsável pelo papel de cliente.

### Fase 1 — consultas, agregações, relacionamentos e views

1. Calcular a quantidade de dependentes.
2. Calcular a quantidade de dependentes por sexo.
3. Calcular a quantidade de clientes da região Sul.
4. Apresentar uma descrição breve dos produtos: código, nome e tipo.
5. Identificar os cinco produtos mais vendidos em quantidade no ano de 2021.
6. Apresentar o nome original, em maiúsculas e em minúsculas dos vendedores do sexo feminino.
7. Apresentar o nome e a idade de todos os dependentes, do mais velho para o mais novo.
8. Calcular o valor total de vendas concluídas e não deletadas por estado.
9. Calcular o total de unidades vendidas, considerando vendas concluídas e não deletadas, por produto.
10. Calcular a média do valor total de vendas por estado.
11. Listar os nomes dos clientes que compram o produto de código 1.
12. Identificar a quantidade mínima e o respectivo produto, explicitando a medida considerada.
13. Apresentar uma descrição detalhada dos produtos: código, nome, tipo e quantidade em estoque.
14. Relacionar os vendedores às vendas realizadas, apresentando código da venda, data da venda, produto e nome do vendedor.
15. Criar uma view com os nomes dos vendedores e seus respectivos filhos/dependentes, incluindo nome e data de nascimento dos dependentes.
16. Criar uma view com informações de vendas, produtos, estoque, clientes e vendedores, considerando apenas vendas concluídas e não deletadas.
17. Criar uma view com a quantidade de vendas por canal.

### Fase 2 — condicionais, combinação de resultados e enriquecimento

1. Filtrar a tabela de vendedores pelo nome `Vendedor 6`.
2. Retornar os nomes dos dependentes, substituindo o nome do dependente de código 5 pelo seu próprio nome no resultado da consulta, usando `IF` ou `CASE`.
3. Unir as vendas do período de **07/05/2019 a 03/03/2021** às vendas do período de **11/09/2011 a 03/09/2012**.
4. Retornar os cinco primeiros caracteres do nome do produto e a quantidade vendida formatada com dez dígitos, preenchendo com zeros à esquerda.
5. Identificar o produto com a maior quantidade vendida no canal `Ecommerce`.
6. Verificar se existem vendas de produtos com status `MVP - validação` e identificar quais são.
7. Calcular quantas vendas estão deletadas logicamente.
8. Calcular quantas vendas estão canceladas.
9. Relacionar o código INEP da escola de cada dependente ao nome da escola, utilizando o [CSV do Censo Escolar 2020](sales.z/Censo2020_inep.csv).

## Como documentar a entrega

A entrega pode ser organizada no GitHub ou em outra ferramenta de documentação. O objetivo é permitir que outra pessoa compreenda a pergunta, confira a consulta e interprete o resultado.

Para cada questão, registre:

1. **Pergunta de negócio:** o que precisa ser respondido.
2. **Consulta SQL:** código utilizado, com formatação legível.
3. **Resultado:** tabela, resumo ou captura de tela.
4. **Interpretação:** o que o resultado informa ao cliente.
5. **Regras adotadas:** filtros, tratamento de duplicidades, datas de referência e outras decisões relevantes.

O [modelo de documentação](sales.z/modelo_doc.md) serve como referência de formato. Revise e adapte as consultas de exemplo à pergunta e ao esquema da base utilizada.

## Referências e ferramentas

- [MySQL — documentação oficial](https://dev.mysql.com/doc/).
- [MySQL — download](https://dev.mysql.com/downloads/mysql/).
- [MySQL Workbench — download](https://dev.mysql.com/downloads/workbench/).
- [Exemplos de MySQL no navegador — W3Schools](https://www.w3schools.com/mysql/mysql_examples.asp).
- [MongoDB — documentação oficial](https://www.mongodb.com/docs/).
- [Conceitos de banco de dados — Blog do Zouza](https://blogdozouza.wordpress.com/dados/estruturados/banco-de-dados/).
- [SQL para análise de dados — Alex Souza](https://medium.com/@aasouzaconsult/sql-para-an%C3%A1lise-de-dados-2183f746f2e1).
- [Dos dados até a tomada de decisão — Alex Souza](https://medium.com/blog-do-zouza/dos-dados-at%C3%A9-a-tomada-de-decis%C3%A3o-534f61abd3cb).
- [Formatação de documentos no GitHub](https://docs.github.com/pt/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

## Sobre o autor

**Alex Souza** — materiais e projetos voltados ao ensino e à aplicação de dados.

[Portfólio de projetos](https://github.com/aasouzaconsult/portfolio-dados) · [Blog](https://medium.com/blog-do-zouza) · [LinkedIn](https://www.linkedin.com/in/alex-souza/) · [Instagram](https://www.instagram.com/alexsouzamsc/)
