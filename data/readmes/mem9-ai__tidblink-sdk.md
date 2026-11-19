# TiDB Link SDKs

Official, supported SDKs for TiDB Link.

The TypeScript SDK lives in [`typescript/`](typescript/README.md). It targets Node.js
22.12 or newer, uses the platform `fetch` API, and has no
runtime dependencies.

The Python SDK lives in [`python/`](python/README.md). It follows the TypeScript
SDK's features and design with an asyncio API for Python 3.11 or newer. It is
in development and not yet published to PyPI.

- [TypeScript quick start](typescript/README.md#quick-start)
- [Python quick start](python/README.md#quick-start)
- [Examples by scenario and language](examples/README.md)
- [Contributing](CONTRIBUTING.md)
- [Release process](RELEASING.md)
- [Changelog](CHANGELOG.md)
- [Security policy](SECURITY.md)

The SDK is pre-1.0 while the TiDB Link HTTP API remains pre-1.0. Each SDK
release declares its exact service baseline and supported scope. This package
covers Organization/End User/Key provisioning, Template discovery, personal Agent
and Session management, text commands with recoverable final results and continuous
progress, Client Tools, explicit cancellation and checkpoint retry, conversation
history, verified file attachments and downloads, Schedulers, Realtime
Model/Connection preparation, prerecorded audio and User usage reads against one exact service revision.
Resource workflows accept Organization authority with an explicit End User as well
as existing User API Keys.
See the TypeScript README for the supported boundaries
and excluded capabilities.

## Development

```sh
npm install
npm test
```

For the Python SDK, see [`python/README.md`](python/README.md#development).

## License

Apache-2.0. See [LICENSE](LICENSE).
