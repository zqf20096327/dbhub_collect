# Collab-IDE

A browser-based collaborative IDE. Multiple users can open the same project, edit the same file simultaneously, and run commands in an isolated terminal, all without installing anything locally.



https://github.com/user-attachments/assets/198e0505-e7cf-41fa-b9ef-d731da498eeb



---

## Architecture

The system has three long-running services and one ephemeral layer:

- **Go API** (`cmd/api`, port 8080): WebSocket hub manager, REST handlers, auth, file I/O, git commits, Docker orchestration.
- **Node Sync Service** (`internal/sync`, port 3000): holds the authoritative in-memory Yjs CRDT state for all open documents. The Go API talks to it over HTTP.
- **PostgreSQL**: stores users, projects, and project metadata.
- **Alpine sandbox containers**: short-lived, one per open project, spawned on-demand by the Go API through the Docker socket.

![System architecture](docs/diagrams/01-architecture.svg)

---

## Collaboration

Editor collaboration uses [Yjs](https://yjs.dev/) CRDTs. The Go API does not hold document state; it proxies updates to and from the Node sync service via HTTP. Awareness (cursor positions, selections, user labels) follows the same path.

When a user saves a file, the Go API writes the plain-text content to disk and creates a git commit in the project repository.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif',
  'fontSize': '14px',
  'actorBkg': '#313244',
  'actorBorder': '#89b4fa',
  'actorTextColor': '#cdd6f4',
  'actorLineColor': '#6c7086',
  'signalColor': '#89b4fa',
  'signalTextColor': '#cdd6f4',
  'labelBoxBkgColor': '#1e1e2e',
  'labelBoxBorderColor': '#45475a',
  'labelTextColor': '#cdd6f4',
  'loopTextColor': '#cdd6f4',
  'noteBkgColor': '#313244',
  'noteBorderColor': '#a6e3a1',
  'noteTextColor': '#cdd6f4',
  'activationBkgColor': '#45475a',
  'activationBorderColor': '#cba6f7'
}}}%%
sequenceDiagram
    autonumber
    actor UserA as User A
    actor UserB as User B
    participant API as Go Backend Server
    participant Sync as Node Sync Service
    participant Git as Git Repository

    Note over UserA, Git: Connection and Initial Sync

    UserA->>API: WS connect, send "sync" event
    API->>Sync: HTTP GET /document { docId }
    Sync-->>API: { ydoc: base64, awareness: base64 }
    API-->>UserA: WS "sync", full Y.Doc + awareness applied

    UserB->>API: WS connect, send "sync" event
    API->>Sync: HTTP GET /document { docId }
    Sync-->>API: same document state
    API-->>UserB: WS "sync", same Y.Doc state applied

    Note over UserA, Git: Live Document Edit

    UserA->>UserA: Types text in Monaco editor
    UserA->>API: WS "document_update" (binary Yjs delta, base64)
    API->>Sync: HTTP PUT /document { docId, update }
    Sync-->>API: 200 OK, Y.Doc updated in memory
    API->>UserB: WS broadcast "document_update"
    UserB->>UserB: Y.applyUpdate applied, Monaco renders remote edit instantly

    Note over UserA, Git: Cursor and Selection Awareness

    UserA->>UserA: Moves cursor / selects text
    UserA->>API: WS "awareness_update" (cursor position, base64)
    API->>Sync: HTTP PUT /document { docId, awareness }
    Sync-->>API: 200 OK
    API->>UserB: WS broadcast "awareness_update"
    UserB->>UserB: Monaco renders User A cursor with unique color + name label

    Note over UserA, Git: File Save and Git Persistence

    UserA->>API: HTTP PUT /api/files/:id (file content)
    API->>Git: os.WriteFile, write raw text to disk
    API->>Git: git add --all + git commit "update file ..."
    Git-->>API: Commit hash
    API-->>UserA: 200 OK
```

---

## Terminal

Each project gets one Alpine container, spawned when the first user opens the terminal tab and destroyed when the last user disconnects. The Go API owns a single permanent goroutine reading from the Docker PTY stream; all WebSocket clients share that stream.

Commands are synchronised with a marker-based protocol: the API appends `echo <uuid-marker>` after each command, detects the marker in stdout, then emits a `command_eoc` event to the client. Every command execution also creates a git commit.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'fontFamily': 'Inter, ui-sans-serif, system-ui, sans-serif',
  'fontSize': '14px',
  'actorBkg': '#313244',
  'actorBorder': '#fab387',
  'actorTextColor': '#cdd6f4',
  'actorLineColor': '#6c7086',
  'signalColor': '#fab387',
  'signalTextColor': '#cdd6f4',
  'labelBoxBkgColor': '#1e1e2e',
  'labelBoxBorderColor': '#45475a',
  'labelTextColor': '#cdd6f4',
  'noteBkgColor': '#313244',
  'noteBorderColor': '#fab387',
  'noteTextColor': '#cdd6f4',
  'activationBkgColor': '#45475a',
  'activationBorderColor': '#cba6f7'
}}}%%
sequenceDiagram
    autonumber
    actor Client as Client (xterm.js)
    participant API as Go Backend Server
    participant Docker as Docker Daemon Socket
    participant Shell as Alpine Sandbox Container
    participant Vol as Persistence Volume

    Note over Client, Vol: Container Lifecycle, one per project

    Client->>API: WS connect /ws/terminal?projectId=...&token=...
    API->>API: Verify JWT, extract user
    API->>Docker: ContainerCreate (alpine image)
    Docker->>Vol: Mount project volume subpath read-write
    Docker-->>API: Container ID
    API->>Docker: ContainerStart
    API->>Docker: ContainerExecCreate  Cmd: sh -l  Tty: true
    Docker-->>API: Exec ID + hijacked I/O stream
    API->>API: Start permanent reader goroutine (single goroutine owns I/O)
    API-->>Client: WS connection upgraded, shell ready

    Note over Client, Vol: Command Execution

    Client->>API: WS event: command  payload: npm run dev
    API->>API: Acquire isRunning lock, reject if already running
    API->>Shell: Forward command + eoc marker to shell stdin
    Shell->>Shell: Execute inside isolated sandbox
    Shell-->>API: stdout / stderr stream line-by-line
    API-->>Client: WS "command_output_line" events (streamed)
    Shell-->>API: eoc marker detected
    API-->>Client: WS "command_eoc", terminal returns to idle
    API->>Vol: git add --all + git commit "execute command npm run dev"

    Note over Client, Vol: Cleanup, last client disconnects

    Client-->>API: WS disconnect (tab closed / navigate away)
    API->>API: Hub removes client, last client triggers shutdown
    API->>Docker: ContainerRemove (force: true)
    Docker->>Shell: Container destroyed and removed
```

---

## Sandbox Security Model

Each terminal session runs inside a container created with the following constraints (see [`internal/executor/docker.go`](internal/executor/docker.go)):

| Constraint | Value |
|---|---|
| `ReadonlyRootfs` | `true` |
| `CapDrop` | `ALL` |
| `SecurityOpt` | `no-new-privileges:true` |
| Network access | none |
| Writable paths | `/home/developer/workspace` (project volume subpath, rw), `/tmp` (tmpfs, 64 MiB), and `/root` (tmpfs, 256 MiB) |

The project files live in a named Docker volume (`collab-ide_persistence`). Each project is mounted via Docker's volume subpath feature, so a container can only see its own project directory.

---

## Stack

| Layer | Technology |
|---|---|
| Frontend | React 19, TypeScript, Vite, Monaco Editor, xterm.js, Yjs |
| Backend | Go 1.25, httprouter, gorilla/websocket, Docker SDK |
| Sync service | Node.js, Yjs (y-protocols) |
| Database | PostgreSQL 18 |
| Persistence | Docker named volume, one subpath per project |
| Git | go-git; every file save and terminal command creates a commit |
| Auth | JWT (golang-jwt), bcrypt (golang.org/x/crypto) |

---

## Setup

### Prerequisites

- Docker and Docker Compose
- The Docker socket accessible at `/var/run/docker.sock`
- The Alpine image available locally: `docker pull alpine`

### Run

```sh
cp .env.example .env
# Edit .env. At minimum, set JWT_SECRET to something non-default.

docker compose up --build
```

The frontend dev server is not part of the compose file. Run it separately:

```sh
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and proxies API calls to `http://localhost:8080`.

### Environment variables

| Variable | Description |
|---|---|
| `POSTGRES_DSN` | Full PostgreSQL connection string |
| `JWT_SECRET` | Secret used to sign and verify JWTs |
| `PERSISTENCE_DIR` | Path inside the API container where project files are stored (mapped to `/data/persistence` by the compose file) |
| `PORT` | API listen port (default: `8080`) |
| `LIMITER_RPS` / `LIMITER_BURST` | Rate limiter settings |

---

## License

[Apache 2.0](LICENSE)
