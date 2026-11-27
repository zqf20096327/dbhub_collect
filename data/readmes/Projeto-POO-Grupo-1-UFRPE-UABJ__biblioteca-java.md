![Logo](./.github/assets/logo_uabjoteca.png)

![Java versão](https://img.shields.io/badge/Java-17%2B-orange?logo=openjdk&logoColor=white) ![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white) ![Gui Swing](https://img.shields.io/badge/GUI-Swing-006B3F?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0id2hpdGUiPjxwYXRoIGQ9Ik0zIDNoMThjMS4xIDAgMiAuOSAyIDJ2MTRjMCAxLjEtLjkgMi0yIDJIM2MtMS4xIDAtMi0uOS0yLTJWNWMwLTEuMS45LTIgMi0yem0wIDRoMThWNUgzdjJ6bTAgMnYxMGgxOFY5SDN6Ii8+PC9zdmc+) ![Git](https://img.shields.io/badge/Git-F05032?logo=git&logoColor=white) ![Disciplina P2](https://img.shields.io/badge/Disciplina-P2-blue) ![UFRPE UABJ](https://img.shields.io/badge/UFRPE-UABJ-1B2D4F) ![Entrega](https://img.shields.io/badge/Entrega-3_de_4-yellow) ![Licença MIT](https://img.shields.io/badge/licença-MIT-green) 

<br>
<br>

> [!NOTE]
> Projeto desenvolvido pelo **Grupo 1** para compor a **2ª VA** de **Programação 2 (2026.2)**.<br>
> Este Trabalho é vinculado ao Bacharelado em Engenharia da Computação da **Universidade Federal Rural de Pernambuco, Unidade Acadêmica de Belo Jardim (UFRPE/UABJ)**.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Regras de Negócio](#%EF%B8%8F-regras-de-negócio)
- [Conceitos da Programação Orientada a Objetos](#-conceitos-da-programação-orientada-a-objetos)
- [Instalação e Execução](#-instalação-e-execução)
- [Cronograma de Entregas](#-cronograma-de-entregas)

---

## 📖 Sobre o Projeto

O **UABJoteca** é um sistema de gerenciamento de biblioteca desenvolvido em Java com foco na aplicação prática dos pilares da **Programação Orientada a Objetos (POO)**.

O projeto tem como objetivo controlar a circulação de livros do acervo entre diferentes perfis de leitores (**Alunos** e **Professores**), automatizando prazos de devolução, limites de empréstimos simultâneos e cálculo de multas em caso de atraso, com regras de negócio protegidas por exceções customizadas.

Sua estrutura foi planejada de forma modular e orientada a camadas (`modelos`, `gerenciadores`, `excecoes` e `telas`), integrando regras de domínio bem encapsuladas, persistência de dados em **SQLite (JDBC/DAO)**, interface gráfica em **Java Swing** e exportação de relatórios em **CSV**.

---

## ✨ Funcionalidades

| | Funcionalidade | Descrição |
| :---: | :--- | :--- |
| <sub> </sub> | <sub> </sub> | <sub> </sub> |
| 💾 | **Persistência em SQLite** | Criação automática das tabelas (`usuario`, `livro` e `emprestimo`) com integridade referencial na inicialização e armazenamento contínuo dos dados via classes DAO (`LivroDAO`, `UsuarioDAO` e `EmprestimoDAO`). |
| 📚 | **Gerenciamento de Livros (CRUD)** | Cadastro de títulos com ISBN único e total de exemplares, listagem completa, busca por título ou autor, edição (mantendo dados atuais ao pressionar Enter) e remoção segura do acervo. |
| 👥 | **Gerenciamento de Usuários (CRUD)** | Cadastro diferenciado entre **Alunos** e **Professores** com matrícula única, listagem exibindo prazo, taxa de multa e empréstimos ativos, além de edição e remoção com confirmação. |
| 🔄 | **Registro e Exclusão de Empréstimos** | Realização de retiradas por ID de usuário e livro, validando estoque e limite com atualização simultânea no banco e cálculo da data prevista, além da opção de apagar registros de empréstimos. |
| 💸 | **Devolução e Cálculo de Multas** | Encerramento de empréstimos com data atual ou informada manualmente (`AAAA-MM-DD`), apurando automaticamente os dias de atraso, calculando a multa e atualizando saldo de exemplares e limite no banco. |
| ⏰ | **Listagem e Filtros de Empréstimos** | Consulta detalhada dos empréstimos usando os filtros `TODOS`, `ATIVOS`, `ENCERRADOS` e `ATRASADOS`, exibindo status, datas, dias de atraso e multa acumulada ou total. |
| 🛡️ | **Validação e Tratamento no Terminal** | Menu interativo com 13 operações no console, tratamento de entradas inválidas (campos vazios, números ou datas fora do padrão) e exibição amigável de erros de negócio e restrições do banco (`UNIQUE` e `FOREIGN KEY`). |
| <sub> </sub> | <sub> </sub> | <sub> </sub> |

---

## ⚖️ Regras de Negócio

O domínio do sistema aplica políticas distintas conforme a categoria do usuário:

| Perfil | Prazo de Devolução | Multa Diária por Atraso | Limite de Empréstimos Simultâneos |
| :--- | :---: | :---: | :---: |
| <sub> </sub> | <sub> </sub> | <sub> </sub> | <sub> </sub> |
| **Aluno** | 7 dias | R$ 1,00 / dia | 3 empréstimos |
| **Professor** | 15 dias | R$ 0,50 / dia | 5 empréstimos |
| <sub> </sub> | <sub> </sub> | <sub> </sub> | <sub> </sub> |

**Restrições adicionais garantidas por exceções customizadas e pelo banco de dados:**
- `LivroIndisponivelException`: Impede o empréstimo de títulos sem exemplares disponíveis no acervo.
- `LimiteEmprestimosException`: Bloqueia novas retiradas caso o usuário já tenha atingido seu teto de empréstimos ativos.
- `EmprestimoEncerradoException`: Impede o encerramento ou devolução de um empréstimo que já foi concluído anteriormente.
- `OperacaoInvalidaException`: Valida campos obrigatórios e quantidade positiva de exemplares no cadastro/edição, impede duplicidade de ISBN ou matrícula nos gerenciadores, bloqueia a remoção de livros com exemplares emprestados ou usuários com empréstimos ativos e impede reduzir o total de exemplares abaixo dos disponíveis.
- `RegistroNaoEncontradoException`: Sinaliza buscas ou operações sobre IDs inexistentes de usuário, livro ou empréstimo no banco de dados.
- **Integridade de datas e banco (`IllegalArgumentException` e `SQLException`)**: Impede devoluções com data nula ou anterior à data do empréstimo, garante unicidade (`UNIQUE`) para `isbn` e `matricula` e protege o histórico contra exclusões indevidas por chave estrangeira (`FOREIGN KEY ... ON DELETE RESTRICT`).

---

## 🧩 Conceitos da Programação Orientada a Objetos

| Conceito | Onde aparece | Aplicação no Projeto |
| :--- | :--- | :--- |
| <sub> </sub> | <sub> </sub> | <sub> </sub> |
| **Classe Abstrata** | `Usuario` | Define a estrutura base dos leitores e obriga as subclasses a implementarem prazo, taxa, limite e tipo. |
| **Herança e Liskov** | `Aluno` e `Professor` | Estendem `Usuario` sem duplicar código e são reconstruídos do banco e usados de forma intercambiável pelo sistema. |
| **Polimorfismo** | `Emprestimo`, `UsuarioDAO` e `BibliotecaApp` | Chamam `getPrazo()`, `getTaxa()` e `getLimiteMaximo()` via `Usuario` sem usar condicionais nas regras de negócio, além de instanciarem dinamicamente o perfil correto a partir do banco. |
| **Encapsulamento** | `Livro`, `Usuario`, `Emprestimo` e `Conexao` | Atributos privados alterados apenas por métodos controlados (`emprestarExemplar()`, `devolver()`, `somarLimite()`), e configuração da conexão/criação das tabelas isolada em `Conexao`. |
| **Sobrecarga** | `Emprestimo`, `Livro`, `Usuario` e `Gerenciador*` | Múltiplas assinaturas nos construtores (novos registros vs. reconstrução do SQLite) e nos métodos `devolver()`, `encerrarEmprestimo()`, `listarLivros()` e `listarUsuarios()`. |
| **Relacionamentos e Camadas** | `modelos`, `gerenciadores` e `dao` | Agregação de `Usuario` e `Livro` em `Emprestimo`, dependência do enum `FiltroEmprestimos` e separação da persistência JDBC nas classes `LivroDAO`, `UsuarioDAO` e `EmprestimoDAO`. |
| <sub> </sub> | <sub> </sub> | <sub> </sub> |

## 🚀 Instalação e Execução

> [!IMPORTANT]
> Este projeto requer o **Java JDK 17** ou superior instalado na máquina.

### Opção 1: Clonando o Repositório

1. Clone o projeto e acesse a pasta.
2. Execute o arquivo **BibliotecaApp.java** localizado em `src/main/java/telas` em sua IDE de preferência ou através do terminal.

### Opção 2: Pelo Executável

1. Baixe o arquivo `biblioteca-ENTREGA-3.jar` [aqui](https://github.com/Projeto-POO-Grupo-1-UFRPE-UABJ/biblioteca-java/releases/tag/entrega3).
2. Abra o terminal na pasta onde o arquivo foi salvo e execute o seguinte comando:

   ```bash
   java -jar biblioteca-ENTREGA-3.jar
   ```

### Opção 3: Banco de Dados Pré-populado (Opcional)

Caso queira testar o sistema imediatamente com dados já cadastrados:

1. Na mesma [página da release](https://github.com/Projeto-POO-Grupo-1-UFRPE-UABJ/biblioteca-java/releases/tag/entrega3), baixe o arquivo `biblioteca.db`, que já contém livros, usuários e empréstimos pré-cadastrados.
2. Mova o arquivo `biblioteca.db` para a mesma pasta onde você salvou o `biblioteca-ENTREGA-3.jar` (ou para a pasta raiz do projeto, caso execute pelo código-fonte).
3. Execute o programa normalmente, o sistema carregará os dados existentes automaticamente.

---

## 📆 Cronograma de Entregas

- [x] **Entrega 1 (`06/11`) - Modelagem:** Diagrama UML e protótipos de tela. [<kbd>🏷️ entrega1</kbd>](https://github.com/Projeto-POO-Grupo-1-UFRPE-UABJ/biblioteca-java/tree/entrega1)
- [X] **Entrega 2 (`26/11`) - Núcleo do Domínio:** Classes de modelo, regras de negócio aplicadas, exceções e main funcional no terminal. [<kbd>🏷️ entrega2</kbd>](https://github.com/Projeto-POO-Grupo-1-UFRPE-UABJ/biblioteca-java/tree/entrega2)
- [X] **Entrega 3 (`26/11`) - Persistência:** Integração com banco SQLite, criação automática de tabelas e classes DAO. [<kbd>🏷️ entrega3</kbd>](https://github.com/Projeto-POO-Grupo-1-UFRPE-UABJ/biblioteca-java/tree/entrega3)
- [ ] **Entrega 4 (`03/12`) - Versão Final:** Interface gráfica completa em Swing, tratamento visual de erros e exportação CSV. <kbd>🏷️ entrega4</kbd>
