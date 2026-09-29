# LitheChat Backend

Backend da plataforma **LitheChat**, uma aplicação de mensagens privadas em tempo real construída com **PHP**, **LithePHP**, **MySQL**, **Redis** e **Workerman**.

O projeto foi desenvolvido para demonstrar como o **Lithe**, framework PHP, pode ser utilizado na construção de uma aplicação moderna, combinando uma API HTTP tradicional com comunicação em tempo real através de WebSockets.

---

## ✨ Funcionalidades

* 🔐 Autenticação de utilizadores
* 👤 Gestão de utilizadores
* 💬 Conversas privadas
* 📨 Envio e recebimento de mensagens
* ⚡ Mensagens em tempo real via WebSocket
* 🔴 Redis Pub/Sub para distribuição de eventos
* 👁️ Marcação de mensagens como lidas
* 🗑️ Remoção de mensagens
* 🛡️ Validação e autorização de acesso às conversas
* 🔄 Comunicação entre API e servidor WebSocket através do Redis

---

## 🏗️ Arquitetura

O backend separa a responsabilidade da API HTTP da comunicação em tempo real.

```text
                         ┌─────────────────────┐
                         │       Frontend      │
                         │       Next.js       │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                  HTTP                          WebSocket
                    │                               │
                    ▼                               ▼
          ┌─────────────────┐             ┌─────────────────┐
          │    LithePHP     │             │    Workerman    │
          │      API        │             │    WebSocket    │
          └────────┬────────┘             └────────┬────────┘
                   │                               │
                   │                               │
                   ▼                               ▼
             ┌───────────┐                  ┌───────────┐
             │   MySQL   │                  │   Redis   │
             │  Database │                  │  Pub/Sub  │
             └───────────┘                  └─────┬─────┘
                                                  │
                                                  │
                                                  ▼
                                         conversation:{id}
```

### Responsabilidades

**LithePHP**

Responsável pela API HTTP, autenticação, autorização, persistência e regras de negócio.

**MySQL**

Responsável pela persistência dos utilizadores, conversas e mensagens.

**Redis**

Funciona como Message Broker através do Pub/Sub.

**Workerman**

Mantém as conexões WebSocket e distribui os eventos em tempo real para os clientes inscritos.

---

## 💬 Fluxo de uma mensagem

Quando um utilizador envia uma mensagem:

```text
Frontend
   │
   │ POST /conversations/{id}/messages
   ▼
LithePHP API
   │
   ├── Autentica utilizador
   ├── Valida conversa
   ├── Cria mensagem
   └── Salva no MySQL
   │
   ▼
RedisPublisher
   │
   │ PUBLISH conversation:{id}
   ▼
Redis
   │
   ▼
Workerman
   │
   │ WebSocket
   ▼
Clientes inscritos
```

A API é responsável pela persistência.

O Redis transporta o evento.

O Workerman entrega o evento aos clientes conectados.

---

## 🧰 Stack

| Tecnologia | Utilização                           |
| ---------- | ------------------------------------ |
| PHP        | Linguagem principal                  |
| LithePHP   | Framework HTTP                       |
| MySQL      | Banco de dados                       |
| Redis      | Message Broker / Pub/Sub             |
| Workerman  | Servidor WebSocket                   |
| Predis     | Cliente Redis                        |
| Composer   | Gerenciamento de dependências        |
| Docker     | Execução do Redis em desenvolvimento |

---

# 🚀 Instalação

## Requisitos

Para executar o backend localmente:

* PHP 8.4+
* Composer
* MySQL 8+
* Redis
* Docker (opcional, utilizado para executar o Redis)

---

## 1. Clonar o projeto

```bash
git clone <repository-url>

cd lithechat
```

---

## 2. Instalar dependências

```bash
composer install
```

---

## 3. Configurar o ambiente

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Configure as variáveis:

```env
APP_NAME=Chat
APP_KEY=jIusvTGrk8VHYmQKx8cHhXyF2DfRwRx33RbZRDQFXFU=
APP_PRODUCTION_MODE=false

JWT_SECRET=8f7c9d2a4e6b1c0f9a3d7e5b2c8f4a1d6e9b3c7f0a5d2e8

REDIS_HOST=127.0.0.1
REDIS_PORT=6379

DB_CONNECTION_METHOD=eloquent
DB_CONNECTION=mysql
DB_HOST=localhost
DB_NAME=lithe_chat
DB_USERNAME=root
DB_PASSWORD=250483
DB_SHOULD_INITIATE=true

WS_HOST=0.0.0.0
WS_PORT=8080
```

> No Windows, o comando `cp` pode ser substituído por `copy .env.example .env`.

---

# 🗄️ MySQL

O MySQL é executado **localmente**, fora do Docker.

Crie o banco:

```sql
CREATE DATABASE lithechat;
```

Depois execute as migrations:

```bash
php line migrate
```

O backend utilizará:

```text
Host:     127.0.0.1
Port:     3306
Database: lithechat
```

---

# 🔴 Redis

O Redis é utilizado como Message Broker entre a API e o servidor WebSocket.

Para facilitar o desenvolvimento, o Redis pode ser executado através do Docker.

```bash
docker run --name lithechat-redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

Verifique se o container está rodando:

```bash
docker ps
```

Deverá aparecer:

```text
lithechat-redis
```

A aplicação conecta-se ao Redis através de:

```env
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

---

# ▶️ Executando o backend

A API e o servidor WebSocket são processos independentes.

## API

```bash
php line serve
```

A API ficará disponível em:

```text
http://localhost:8000
```

## WebSocket

Em outro terminal:

```bash
php websocket start
```

O servidor WebSocket ficará disponível em:

```text
ws://localhost:8080
```

## Redis

Caso esteja utilizando Docker:

```bash
docker start lithechat-redis
```

---

# ⚡ WebSocket

O servidor WebSocket utiliza canais individuais para cada conversa.

Exemplo:

```text
conversation:15
```

Quando o utilizador abre a conversa `15`, o frontend envia:

```json
{
  "type": "subscribe",
  "channel": "conversation:15"
}
```

Para sair:

```json
{
  "type": "unsubscribe",
  "channel": "conversation:15"
}
```

O Workerman mantém uma lista das conexões inscritas em cada canal.

---

# 📡 Eventos em tempo real

Os eventos publicados pela API no Redis possuem o seguinte formato:

```json
{
  "event": "message.created",
  "data": {
    "message": {}
  }
}
```

## `message.created`

Disparado quando uma nova mensagem é criada.

```json
{
  "event": "message.created",
  "data": {
    "message": {
      "id": 25,
      "conversation_id": 15,
      "user_id": 2,
      "content": "Olá!",
      "created_at": "2026-08-25T20:00:00"
    }
  }
}
```

## `message.deleted`

Disparado quando uma mensagem é removida.

```json
{
  "event": "message.deleted",
  "data": {
    "id": 25
  }
}
```

## `messages.read`

Disparado quando as mensagens são marcadas como lidas.

```json
{
  "event": "messages.read",
  "data": {
    "user_id": 2
  }
}
```

---

# 🔗 API

## Autenticação

```text
POST /api/auth/register
POST /api/auth/login
```

## Utilizadores

```text
GET /api/users
```

## Conversas

```text
GET  /api/conversations
POST /api/conversations
```

## Mensagens

```text
GET    /api/conversations/{conversationId}/messages
POST   /api/conversations/{conversationId}/messages
POST   /api/conversations/{conversationId}/messages/read
DELETE /api/messages/{id}
```

As rotas protegidas requerem autenticação através de:

```http
Authorization: Bearer <token>
```

---

# 📨 Enviar mensagem

Exemplo:

```http
POST /api/conversations/15/messages
Authorization: Bearer <token>
Content-Type: application/json
```

Body:

```json
{
  "content": "Olá, tudo bem?"
}
```

Resposta:

```json
{
  "message": {
    "id": 25,
    "conversation_id": 15,
    "user_id": 2,
    "content": "Olá, tudo bem?",
    "created_at": "2026-08-25T20:00:00"
  }
}
```

Depois de salvar a mensagem no MySQL, a API publica o evento:

```text
conversation:15
```

O Workerman recebe o evento através do Redis e envia a mensagem para os clientes inscritos nesse canal.

---

# 🔐 Segurança

Antes de executar operações sobre uma conversa, o backend verifica se o utilizador autenticado pertence à mesma.

Exemplo:

```php
$conversation = $user->conversations()
    ->where(
        'conversations.id',
        $conversationId
    )
    ->first();
```

Isso impede que um utilizador autenticado aceda às mensagens de uma conversa da qual não participa.

---

# 🔄 Modelo de comunicação

O LitheChat utiliza três formas principais de comunicação.

### HTTP

Utilizado para:

* autenticação;
* carregar utilizadores;
* carregar conversas;
* carregar mensagens;
* criar mensagens;
* apagar mensagens;
* marcar mensagens como lidas.

### WebSocket

Utilizado para:

* novas mensagens;
* mensagens removidas;
* mensagens marcadas como lidas;
* eventos em tempo real.

### Redis Pub/Sub

Responsável por transportar os eventos entre a API e o servidor WebSocket.

```text
             HTTP
Frontend ──────────────► LithePHP
                           │
                           │ MySQL
                           ▼
                         MySQL

                           │
                           │ Redis Publish
                           ▼
                         Redis
                           │
                           │ Redis Subscribe
                           ▼
                       Workerman
                           │
                           │ WebSocket
                           ▼
                       Frontend
```

---

# 🧪 Desenvolvimento

Para trabalhar no projeto, execute os componentes necessários separadamente.

### Terminal 1 — API

```bash
php line serve
```

### Terminal 2 — WebSocket

```bash
php line websocket
```

### Docker — Redis

```bash
docker start lithechat-redis
```

Caso o container ainda não exista:

```bash
docker run --name lithechat-redis \
  -p 6379:6379 \
  -d redis:7-alpine
```

### Migrations

Sempre que necessário:

```bash
php line migrate
```

---

# 🧩 Arquitetura de eventos

O fluxo de uma mensagem em tempo real é:

```text
1. Utilizador A envia mensagem
            │
            ▼
2. POST /api/conversations/{id}/messages
            │
            ▼
3. LithePHP valida a requisição
            │
            ▼
4. Mensagem é persistida no MySQL
            │
            ▼
5. RedisPublisher publica o evento
            │
            ▼
6. Redis recebe o evento
            │
            ▼
7. Workerman recebe através do Pub/Sub
            │
            ▼
8. Workerman encontra os clientes inscritos
            │
            ▼
9. Evento é enviado através do WebSocket
            │
            ▼
10. Frontend atualiza a conversa
```

Essa arquitetura permite manter a persistência e as regras de negócio na API enquanto a comunicação em tempo real permanece isolada no servidor WebSocket.

---

# 🎯 Objetivo do projeto

O LitheChat foi criado como um projeto de estudo e demonstração para mostrar, na prática, como o **Lithe**, framework PHP desenvolvido por mim, pode ser utilizado na construção de uma aplicação real.

O projeto explora diferentes aspectos do desenvolvimento backend, incluindo:

* APIs HTTP;
* autenticação;
* autorização;
* persistência relacional;
* WebSockets;
* Redis Pub/Sub;
* comunicação em tempo real;
* organização modular;
* integração entre diferentes componentes;
* arquitetura orientada a eventos.

Mais do que uma aplicação de mensagens, o LitheChat funciona como um projeto de referência para demonstrar as capacidades do **Lithe na construção de aplicações modernas em PHP**.

---

## 📄 Licença

Este projeto é destinado principalmente a fins de estudo e demonstração.
