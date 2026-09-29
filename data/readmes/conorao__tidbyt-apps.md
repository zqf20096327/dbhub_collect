# tidbyt-apps

A collection of [Tidbyt](https://tidbyt.com) applets written in Starlark. Hopefully, these will also be compatible with the new firmware [Niblet](https://www.heyniblet.com/) as well, considering that Tidbyt has been acquired and some services have been shutting down.

## Description

This repo holds Tidbyt apps that render on a 64×32 LED display.

### Included apps:
[**demo.star**](demo.star) fetches recent Bitcoin market prices from Blockchain.info and shows the latest value next to a BTC icon.

## Getting Started

### Prerequisites

- [Pixlet](https://github.com/tidbyt/pixlet) (the Tidbyt applet runtime and renderer)
- Python 3.11 (see `.python-version`) if you use Pixlet’s Python-based tooling

### Installation

```bash
git clone <repo-url>
cd tidbyt-apps
```

Install Pixlet following the official [Pixlet installation guide](https://tidbyt.dev/docs/build/installing-pixlet).

## Usage

Preview the demo applet locally:

```bash
pixlet serve demo.star
```

Render a still image:

```bash
pixlet render demo.star
```

Push to a Tidbyt device (requires a device ID and API token):

```bash
pixlet push --api-token <token> <device-id> demo.webp
```

## Contributing

Contributions are welcome. Open an issue or pull request with a clear description of the change.

## License

MIT
