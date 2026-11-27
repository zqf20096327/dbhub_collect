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
release declares its exact service baseline and supported scope. The SDKs
cover End User provisioning, Template and Skill management, Connectors, Session
management, text commands with recoverable final results and continuous
progress, Client Tools and Session connections, File Notifications and reads
of files in a Session's Drive, explicit cancellation and checkpoint retry,
conversation history, verified file attachments and downloads, Realtime
Model/Connection preparation, prerecorded audio and User usage reads against
one exact service revision. Every resource workflow uses an Organization API
Key with an explicitly selected End User; User API Keys are not supported. See
[the TypeScript README](typescript/README.md#supported-scope) for the supported
boundaries and excluded capabilities.

## Development

```sh
npm install
npm test
```

For the Python SDK, see [`python/README.md`](python/README.md#development).

## License

Apache-2.0. See [LICENSE](LICENSE).
