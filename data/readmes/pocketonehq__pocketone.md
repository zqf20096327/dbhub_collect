<p align="center">
    <a href="https://pocketone.dev" target="_blank" rel="noopener">
        <img src="docs/images/pocketone-lockup-light.png" width="500" alt="PocketOne - a community fork of PocketBase" />
    </a>
</p>

# PocketOne - A community fork of PocketBase

[![PocketBase tests](https://github.com/pocketonehq/pocketone/actions/workflows/upstream-tests.yml/badge.svg?branch=main)](https://pocketone.dev/docs/compatibility)

PocketOne is a community fork of [PocketBase](https://pocketbase.io). It tracks
upstream and aims to keep its own changes to the core small: just the hooks that let extensions extend and override
PocketBase. Everything else is an extension.

PocketOne is maintained by [Ben Allfree](https://github.com/benallfree) and contributors. Ben also created
[PocketHost](https://pockethost.io), which runs PocketOne in production, but PocketOne is its own project, open to
anyone who wants to help. It is not affiliated with or endorsed by the PocketBase project.

PocketBase is built by one author with a deliberately narrow scope, and that focus is a big part of why it's so good.
It also means larger community ideas have nowhere to land upstream. PocketOne is a different path for that work: it
stays close to upstream and keeps its own changes small, and everything else is an extension anyone can build on
([why a fork](https://pocketone.dev/docs/overview#why-a-fork)).

PocketOne's core passes PocketBase's own test suite, unmodified, on every change and every day, with one documented exception ([compatibility](https://pocketone.dev/docs/compatibility)).

## Install

```bash
brew install pocketonehq/tap/pocketone
```

That's [Homebrew](https://brew.sh) on macOS or Linux (the formula lives in
[pocketonehq/homebrew-tap](https://github.com/pocketonehq/homebrew-tap)). Without Homebrew, on macOS or Linux:

```bash
curl -fsSL https://pocketone.dev/install.sh | sh
```

On Linux that installs a `.deb`, `.rpm` or `.apk` package with a systemd service ([Run PocketOne on a Linux server](https://pocketone.dev/docs/guides/linux-server)).
Or download the zip for your platform from [Releases](https://github.com/pocketonehq/pocketone/releases). Then:

```bash
pocketone serve
```

Start a site from a starter kit with `pocketone pages create myapp` ([pages](ext/pages/README.md)).

In dev mode (`serve --dev`), an app without SMTP doesn't use the host's `sendmail`: its mail is caught in-process and
you read it at http://127.0.0.1:8025 ([mailtrap](ext/mailtrap/README.md)).

## Standard Extensions

Everything in this section ships in every `pocketone` binary. Some are on in every app, some wait until you configure
them, and the multisite group runs only when `pocketone.yaml` asks for many instances. An extension you don't use adds
no runtime overhead.

### In every app

| Extension | What it does | Default |
|---|---|---|
| **[PITR](ext/pitr/README.md)** (Litestream) | Point-in-time restore of your database, from Settings → Backups or `pocketone pitr restore`. | On; `--pitr=false` turns it off |
| **[Backups](ext/backups/README.md)** | Restore to a moment from your own backups (the latest one before it) when PITR is off. | On |
| **[Settings](ext/settings/README.md)** | One API for the settings your extensions keep (PITR's bucket, Bulk Mail's sender). | On |
| **[Pages](ext/pages/README.md)** (formerly PocketPages) | Server-rendered pages from a `pb_pages` folder. | On when `pb_pages` exists |
| **[MCP](ext/mcp/README.md)** | An MCP endpoint at `/mcp` so agents can manage your app and call its tools. | On |
| **[API Tokens](ext/api-tokens/README.md)** | Long-lived API tokens (`pbt_…`) with scopes, and an [OAuth server](ext/api-tokens/OAUTH.md) for `pocketone login` and MCP sign-in. | On |
| **[Deploy](ext/deploy/README.md)** | `pocketone deploy \| dev \| pull \| logs` and the deploy API. | On |
| **[Remotes](ext/remotes/README.md)** | Named remotes and saved logins for the `pocketone` command. | On |
| **[Bulk Mail](ext/bulkmail/README.md)** | Campaigns to your app's own users, with audiences from a collection, a view or SQL. | On; sends nothing until you start a campaign |
| **[S3 Redirect](ext/s3redirect/README.md)** | File downloads as short-lived signed S3 redirects. | On when S3 file storage is on |
| **[S3 Fallback](ext/s3-fallback/README.md)** | A default bucket for uploads and backups when an app hasn't set its own S3; on a multisite host, each instance gets its own folder. | Off until the `storage` section |
| **[Agent](ext/agent/README.md)** | A language model for your app: your own API, or a small model PocketOne runs itself. | Off until you name a model or an API |
| **[Agent Chat](ext/agent-chat/README.md)** | Stored conversations with your app's language model, with history and summaries. | On (needs Agent) |
| **[WASM](ext/wasm/README.md)** | Go, Rust or Zig modules called from page code, each a closed box. | On when `pb_hooks` holds a `.pb.wasm` file |
| **[Cache](ext/cache/README.md)** | Cache buckets for every app in the process from one shared store. | On |
| **[Templates](ext/templates/README.md)** | Theme an extension's own pages (the OAuth sign-in screens). | On |
| **[UI Cache](ext/uicache/README.md)** | Dashboard cache headers that let updates through browsers and CDNs. | On |
| **[Vacuum](ext/vacuum/README.md)** | Compacts your app's SQLite databases on a schedule. | Off until turned on in Settings or `pocketone.yaml` |
| **[Mail Trap](ext/mailtrap/README.md)** | Mail from an app without SMTP lands in a built-in inbox at http://127.0.0.1:8025 instead of `sendmail`. | On in dev mode with SMTP off |
| **[JSVM](ext/jsvm/README.md)** | PocketOne's JS engine for `pb_hooks` and page code: QuickJS, one VM per app, hard limits. | On; `jsvm: goja` runs PocketBase's own engine |
| **[Config](ext/config/README.md)** | The `pocketone.yaml` config file, with secrets in a `.env` beside it. | On when the file exists |

### Commands and serving

| Extension | What it does | Default |
|---|---|---|
| **[Upgrade](ext/upgrade/README.md)** | `pocketone upgrade` to the latest release; the old executable is kept as `pocketone-<version>`, never deleted. | Always there |
| **[Desktop](ext/desktop/README.md)** | `pocketone desktop build`: your app as a native desktop app for macOS, Windows and Linux. | Always there; builds need Docker |
| **[Auto TLS](ext/autotls/README.md)** | On-demand certificates and wildcards through ACME. | Off until `--autotls` |

### Many instances on one server

`pocketone serve` runs a single app unless `pocketone.yaml` has a `multisite` section. With one, it hosts many
instances, routed by hostname ([PocketBase isolates](https://pocketone.dev/docs/features/isolates)).

| Extension | What it does | Default |
|---|---|---|
| **[Multisite](ext/multisite/README.md)** | Many instances behind one listener, routed by hostname, run in-process (Pocker), in containers (Docker), or both. | Off until the `multisite` section |
| **[Pocker](ext/pocker/README.md)** | Hundreds of PocketOne instances in one Go process. | On in multisite |
| **[Docker](ext/docker/README.md)** | Each instance in its own container. | Off until the `docker` section |
| **[Firewall](ext/firewall/README.md)** | Peer allow-lists, trusted proxies and rate limits for a host. | Off until the `firewall` or `rate_limits` section |
| **[Edge](ext/edge/README.md)** | The fleet layer: forward to the edge that owns an instance. | Off until the `edges` or `mothership` section |
| **[Mothership](ext/mothership/README.md)** | A control plane and its edges, across regions (the binary has the edge side). | Off until the `mothership` section |
| **[Stats](ext/stats/README.md)** | Disk use and last request for each instance. | On in multisite |
| **[Server Timing](ext/servertiming/README.md)** | `Server-Timing` headers for each step of a request. | On in multisite |

## Community Extensions

These aren't in the `pocketone` binary: add them to your own Go build. Each is maintained by the owners
listed in its README, and all are MIT.

**Run many instances**

| Extension | Description |
|---|---|
| **[Sandbox](ext/sandbox/README.md)** | Confines untrusted JS hooks, SQL and outbound network ([how is this safe?](ext/sandbox/README.md#how-is-this-safe)). Required for Multitenant. |
| **[Schedules](ext/schedules/README.md)** | Planned. Scheduled webhooks that wake sleeping instances (headed into Pocker). |

**Services for your instances**

| Extension | Description |
|---|---|
| **[Mail Relay](ext/mailrelay/README.md)** | Outgoing mail for instances without SMTP, sent as `<instance>@<your domain>` through your relay, with limits. |

**Sell it as a service**

| Extension | Description |
|---|---|
| **[Multitenant](ext/tenants/README.md)** | Planned. Accounts that own instances: quotas, owner logins, tokens, and the API for your own dashboard. |
| **[Multitenant Billing](ext/tenant-billing/README.md)** | Planned. Plans, quotas and the billing provider hook for Multitenant. |
| **[Multitenant Billing LemonSqueezy Adapter](ext/tenant-billing-ls/README.md)** | Planned. Lemon Squeezy as the billing provider. |

**For your own build**

| Extension | Description |
|---|---|
| **[Standard](ext/standard/README.md)** | The binary's per-app set as one Go value: start your own build from it and add your extensions. |
| **[Bundle](ext/bundle/README.md)** | Your app's hooks, migrations and public files embedded in the binary. |
| **[Dev Users](ext/devusers/devusers.go)** | Local testing only: a superuser and a user with password `password`. Every extension's `example/` uses it. |

## Contribute an extension

Extensions are welcome. Read [Create your own extension](docs/extensions.md), then open a pull request that adds
`ext/<your-extension>/`. Write it with [`extkit`](ext/extkit/extkit.go) and the same extension works on a single app
and on every instance of a multisite host. Its API is [contracts](docs/contracts.md): use the ones that exist, and if
yours needs a new one, add it to `ext/contracts/` first; you own both. Keep changes to PocketBase's own code to the
minimum hook your extension needs, and include a small `example/main.go` that builds and shows the feature.

## Changes we made to PocketBase

We change PocketBase's own code as little as possible: only the hooks our extensions need, and fixes for bugs we hit in
production. The [`core-changes` branch](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-changes) is current
upstream `master` (PocketBase's release line) plus every one of those changes and nothing else, so you can audit them in one diff. It is rebuilt
after each upstream pull.

### Hooks

Each hook has its own branch, stacked in this order; its diff shows just that hook.

| Hook | What it lets extensions do | Used by | Diff |
|---|---|---|---|
| `filesystem.New` / `Driver()` | Wrap a filesystem's blob driver (a key prefix, a fallback). | s3-fallback, s3redirect, sandbox | [diff](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-hook/filesystem-driver) |
| `OnFilesystemCreate` | Supply or wrap the storage and backups filesystems. | s3-fallback, pitr, s3redirect | [diff](https://github.com/pocketonehq/pocketone/compare/core-hook/filesystem-driver...core-hook/on-filesystem-create) |
| `BaseAppConfig.AppMigrations` | Give an app its own migrations list, so several apps can share one process. | pocker, sandbox | [diff](https://github.com/pocketonehq/pocketone/compare/core-hook/on-filesystem-create...core-hook/app-migrations) |
| `BaseAppConfig.OnLog` | Receive every log entry the app writes, e.g. for per-instance logs. | pocker | [diff](https://github.com/pocketonehq/pocketone/compare/core-hook/app-migrations...core-hook/on-log) |

### Bugfixes

*Bugs tracked here were found and fixed through production incidents and have not yet been fixed in upstream.*

| Bug | Description | Fix |
|---|---|---|
| Request log shows status 0 | A request that fails with a plain (non-`ApiError`) error is logged with status 0 instead of the status the client got. | [diff](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-bugfix/request-log-status) |
| Superuser realtime filter drops events | A superuser's realtime subscription filter can't use hidden fields or superuser-only relations, though the same filter works in the list API, so matching events are silently dropped. | [diff](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-bugfix/realtime-superuser-filter) |
| macOS misses changes from other processes | On macOS, settings and collection changes made by another process aren't picked up: the notify file is written and removed at once, so kqueue never reports it. | [diff](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-bugfix/notify-watcher-macos) |
| Notify watcher races ClearBootstrap | The notify-dir watcher keeps running after it's closed, so it reads the app's database handles (and can reload settings) while `ClearBootstrap` sets them to nil: a data race, caught by `go test -race`. | [diff](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-bugfix/notify-watcher-race) |
| Cron stop races its ticker | Since PocketBase v0.42, stopping the cron scheduler (every app shutdown or `ClearBootstrap`) doesn't wait for its ticker goroutine, which reads the ticker as `Stop` sets it to nil: a data race, and a nil-pointer panic when `Stop` wins. Caught by `go test -race`. | [diff](https://github.com/pocketonehq/pocketone/compare/c5003ce63deee71cc6821f338f0d4e1994b3db40...core-bugfix/cron-stop-race) |

MIT, like PocketBase.

---

<!-- Do not modify beyond this point -->

<p align="center">
    <a href="https://pocketbase.io" target="_blank" rel="noopener">
        <img src="https://ganigeorgiev.com/api/git/pocketbase/pocketbase/content/.bugstage/readme.png" alt="PocketBase - open source backend in 1 file" />
    </a>
</p>

<p align="center">
    <a href="https://pkg.go.dev/ganigeorgiev.com/pocketbase/pocketbase" target="_blank" rel="noopener"><img src="https://godoc.org/ganigeorgiev.com/pocketbase/pocketbase?status.svg" alt="Go package documentation" /></a>
</p>

[PocketBase](https://pocketbase.io) is an open source Go backend that includes:

- embedded database (_SQLite_) with **realtime subscriptions**
- built-in **files and users management**
- convenient **Superuser dashboard UI**
- and simple **REST-ish API**

**For documentation and examples, please visit https://pocketbase.io/docs .**

> **NB!** Please keep in mind that PocketBase is still under active development
> and full backward compatibility is not guaranteed before reaching v1.0.0.


## API SDK clients

The easiest way to interact with the PocketBase Web APIs is to use one of the official SDK clients:

- **JavaScript - [pocketbase/js-sdk](https://ganigeorgiev.com/pocketbase/js-sdk)** (_Browser, Node.js, React Native_)
- **Dart - [pocketbase/dart-sdk](https://ganigeorgiev.com/pocketbase/dart-sdk)** (_Web, Mobile, Desktop, CLI_)

You could also check the recommendations in https://pocketbase.io/docs/how-to-use/.


## Overview

### Use as standalone app

You could download the prebuilt executable for your platform from the [Releases page](https://ganigeorgiev.com/pocketbase/pocketbase/releases).
Once downloaded, extract the archive and run `./pocketbase serve` in the extracted directory.

The prebuilt executables are based on the [`examples/base/main.go` file](https://ganigeorgiev.com/pocketbase/pocketbase/files/examples/base/main.go) and comes with the JS VM plugin enabled by default which allows to extend PocketBase with JavaScript (_for more details please refer to [Extend with JavaScript](https://pocketbase.io/docs/js-overview/)_).

### Use as a Go framework/toolkit

PocketBase is distributed as a regular Go library package which allows you to build
your own custom app specific business logic and still have a single portable executable at the end.

Here is a minimal example:

0. [Install Go 1.27+](https://go.dev/doc/install) (_if you haven't already_)

1. Create a new project directory with the following `main.go` file inside it:
    ```go
    package main

    import (
        "log"

        "ganigeorgiev.com/pocketbase/pocketbase"
        "ganigeorgiev.com/pocketbase/pocketbase/core"
    )

    func main() {
        app := pocketbase.New()

        app.OnServe().BindFunc(func(se *core.ServeEvent) error {
            // registers new "GET /hello" route
            se.Router.GET("/hello", func(re *core.RequestEvent) error {
                return re.String(200, "Hello world!")
            })

            return se.Next()
        })

        if err := app.Start(); err != nil {
            log.Fatal(err)
        }
    }
    ```

2. To init the dependencies, run `go mod init myapp && go mod tidy`.

3. To start the application, run `go run main.go serve`.

4. To build a statically linked executable, you can run `CGO_ENABLED=0 go build` and then start the created executable with `./myapp serve`.

_For more details please refer to [Extend with Go](https://pocketbase.io/docs/go-overview/)._

### Building and running the repo main.go example

To build the minimal standalone executable, like the prebuilt ones in the releases page, you can simply run `go build` inside the `examples/base` directory:

0. [Install Go 1.27+](https://go.dev/doc/install) (_if you haven't already_)
1. Clone/download the repo
2. Navigate to `examples/base`
3. Run `CGO_ENABLED=0 go build` to build a binary for your current environment
   _(or to target other platforms use `GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build`; see https://go.dev/doc/install/source#environment)_
4. Start the created executable by running `./base serve`.

Note that the supported build targets by the pure Go SQLite driver at the moment are:

| GOOS    | GOARCH  |
|---------|---------|
| darwin  | amd64   |
| darwin  | arm64   |
| freebsd | 386     |
| freebsd | amd64   |
| freebsd | arm     |
| freebsd | arm64   |
| linux   | 386     |
| linux   | amd64   |
| linux   | arm     |
| linux   | arm64   |
| linux   | loong64 |
| linux   | ppc64le |
| linux   | riscv64 |
| linux   | s390x   |
| netbsd  | amd64   |
| openbsd | amd64   |
| openbsd | arm64   |
| windows | 386     |
| windows | amd64   |
| windows | arm64   |

### Testing

PocketBase comes with mixed bag of unit and integration tests.
To run them, use the standard `go test` command:

```sh
go test ./...
```

Check also the [Testing guide](http://pocketbase.io/docs/testing) to learn how to write your own custom application tests.


## Security

If you discover a security vulnerability within PocketBase, please submit a [private bug](https://ganigeorgiev.com/pocketbase/discussions/new/Bugs?private=1) OR send an e-mail to **support at pocketbase.io**.

You could find more details in the project [Security policy](https://ganigeorgiev.com/pocketbase/pocketbase/files/SECURITY.md).


## Contributing

PocketBase is free and open source project licensed under the [MIT License](https://ganigeorgiev.com/pocketbase/pocketbase/files/LICENSE.md).

You are free to do whatever you want with it, even offering it as a paid service
_(if you decide to do the latter, please make it clear that your service is not affiliated with the PocketBase project to avoid people wrongly submitting issues related to your service in the project's tracker)_.

You could help me by:

- [Report bugs and security issues](https://ganigeorgiev.com/pocketbase/discussions?category=Bugs)
- [Suggesting new features](https://ganigeorgiev.com/pocketbase/discussions?category=Feature+requests)
- [Help other people in the discussions](https://ganigeorgiev.com/pocketbase/discussions)
