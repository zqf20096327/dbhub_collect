# SSH MCP Server

[![smithery badge](https://smithery.ai/badge/@KinoThe-Kafkaesque/ssh-mcp-server)](https://smithery.ai/server/@KinoThe-Kafkaesque/ssh-mcp-server)

A Model Context Protocol (MCP) server implementation that provides SSH
capabilities. This server allows for secure remote access and execution through
the MCP protocol.

## Features

- SSH server implementation using MCP protocol
- SQLite database integration for data persistence
- TypeScript implementation for type safety and better development experience

## Prerequisites

- Node.js 18 or higher
- npm or yarn package manager
- TypeScript knowledge for development

## Installation

### Installing via Smithery

To install SSH Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@KinoThe-Kafkaesque/ssh-mcp-server):

```bash
npx -y @smithery/cli install @KinoThe-Kafkaesque/ssh-mcp-server --client claude
```

### Manual Installation
1. Clone the repository:

```bash
git clone <repository-url>
cd ssh-server
```

2. Install dependencies:

```bash
npm install
```

3. Build the project:

```bash
npm run build
```

## Usage

### Configuration

The server uses a SQLite database (`ssh.db`) to store SSH credentials. The
database file will be created automatically when the server starts.

### Tools

The server stores named credentials, then every remote action refers to a
`credentialName`. `privateKeyPath` must point to an existing private key
(`~/` expands to your home directory).

Host keys are verified: the first time a credential connects, the server's
host key fingerprint is pinned in `~/ssh.db`. Later connections that present a
different key are refused with `HOST_KEY_MISMATCH`. To pin a known key up
front, pass `hostKeyFingerprint` (the `SHA256:...` value printed by
`ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` on the server). After a
legitimate key change, remove the credential and add it again.

- `add_credential`: save `{ "name", "host", "username", "privateKeyPath", "hostKeyFingerprint"? }`.
- `list_credentials`: list stored credential records.
- `remove_credential`: delete `{ "name" }`.
- `ssh_exec`: run a shell command with `{ "credentialName", "command", "timeout" }`.
- `ssh_exec_raw`: run an argv-style command array, for example `{ "credentialName": "prod", "command": ["grep", "-E", "foo|bar", "/var/log/app.log"] }`.
- `scp_copy`: copy one file over SFTP with `{ "credentialName", "localPath", "remotePath", "direction" }`.
- `rsync_copy`: copy directories or larger trees with rsync and the same transfer shape.
- `ssh_session_start`, `ssh_session_send`, `ssh_session_read`, `ssh_session_end`, `ssh_session_list`: manage interactive SSH sessions.
- `ssh_tunnel_start`, `ssh_tunnel_list`, `ssh_tunnel_stop`: manage local or remote port-forwarding tunnels.

Example:

```json
{
  "tool_name": "ssh_exec",
  "arguments": {
    "credentialName": "prod",
    "command": "uptime",
    "timeout": 120000
  }
}
```

### Starting the server

```bash
npm start
```

The server will start running on the configured port (default settings can be
modified in the source code).

## CLI Usage

The CLI shares the MCP server's `~/ssh.db` credential store. For remote work it
uses an OpenSSH multiplexed connection, so separate CLI invocations for the
same host, username, and key reuse one authenticated transport. Build first,
then run with `npm run cli --` or via the `sshcli` bin after `npm link`:

```bash
npm run build && npm run cli -- <command>
# or, after linking:
npx sshcli <command>
```

Commands:

```bash
sshcli creds add prod --host 1.2.3.4 --user ubuntu --key ~/.ssh/id_rsa
sshcli creds list
sshcli creds rm prod
sshcli exec prod uptime
sshcli exec prod --timeout 30000 -- df -h /
sshcli exec --raw prod grep -E 'foo|bar' /var/log/app.log
sshcli scp prod ./file.txt /tmp/file.txt toRemote
sshcli rsync prod ./dir/ /tmp/dir/ fromRemote
sshcli session prod   # live interactive shell; Ctrl+D or exit to close
sshcli tunnel prod --type local --local-port 8080 --remote-host localhost --remote-port 80
sshcli cache status prod
sshcli cache close prod
```

Notes:
- For `exec`, the variadic `<command...>` is greedy, so put options like
  `--timeout` and `--raw` *before* the command tokens.
- `exec`, `scp`, `rsync`, `session`, and `tunnel` all reuse the same connection.
  Idle connections remain cached for 30 minutes by default.
- The first connection attempt for an endpoint is serialized across CLI
  processes. A failed attempt creates a 15-second exponential reconnect
  backoff (up to 5 minutes), preventing repeated calls from hammering a
  rate-limited host.
- `session` and `tunnel` are foreground commands that block until the shell
  closes or you press Ctrl+C, respectively; exiting them does not close the
  shared transport.
- The CLI intentionally omits session send/read/end/list and tunnel list/stop
  commands: their in-memory state does not persist across one-shot CLI
  invocations. Use the foreground `session` and `tunnel` commands instead.
- The cache lives under `$XDG_RUNTIME_DIR/sshcli/connections` (or a private
  per-user temporary directory). Tune it with
  `SSHCLI_CONTROL_PERSIST_SECONDS`, `SSHCLI_RECONNECT_BACKOFF_MS`,
  `SSHCLI_RECONNECT_BACKOFF_MAX_MS`, or `SSHCLI_CACHE_DIR`.
- OpenSSH, scp, and rsync must be available in `PATH` for their corresponding
  CLI commands.

## Project Structure

- `src/` - Source code directory
- `build/` - Compiled JavaScript output
- `node_modules/` - Project dependencies

## Dependencies

- `@modelcontextprotocol/sdk`: MCP protocol implementation
- `sqlite3`: SQLite database driver
- `typescript`: Development dependency for TypeScript support

## Development

To make changes to the project:

1. Make your changes in the `src/` directory
2. Rebuild the project:

```bash
npm run build
```

3. Start the server to test your changes:

```bash
npm start
```

## License

MIT

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
