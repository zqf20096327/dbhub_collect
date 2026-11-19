# goscan

Network enumeration often means running separate commands for host discovery, port scans, and service checks. goscan provides an interactive client for nmap with auto-completion and a shared view of scan results, so you can work through those steps without tracking every command by hand.

## Features

- Load targets from CIDR entries, text files, or folders.
- Run host discovery and port scans through nmap.
- Store scan state in SQLite and import discovery or port-scan results at different stages.
- Run scans in the background, detached from the interactive client.
- Enumerate detected services with external tools such as nikto, enum4linux, and Hydra.
- Preview service-enumeration commands with the `DRY` mode before executing them.

## Installation

The source build uses Docker Compose, Make, and the project's Go build environment. From a checkout of this repository, start the build environment:

```bash
docker-compose up --build
docker-compose run cli /bin/bash
```

Inside the container, initialize dependencies and build:

```bash
make init
make setup
make build
```

Place the resulting `goscan` executable in a directory on your `PATH`. Install nmap on the machine where scans will run. Service-specific checks also require their external tools to be installed and available on `PATH`.

## Usage

**Scan only systems you own or have explicit permission to test.** Review scan settings before use; aggressive enumeration can invoke credential attacks and other intrusive checks.

Start the interactive client:

```bash
goscan
```

At the goscan prompt, load an authorized target and inspect the target list:

```text
load target SINGLE 192.0.2.10/32
show targets
```

Use auto-completion to select the scan type and target for discovery and port scans. The command forms are:

```text
sweep <TYPE> <TARGET>
portscan <TYPE> <TARGET>
```

You can also import an existing nmap XML result and inspect the discovered hosts and ports:

```text
load portscan /path/to/nmap-results.xml
show hosts
show ports
```

Before running service enumeration, preview the commands with:

```text
enumerate <TYPE> DRY <TARGET>
```

Replace the angle-bracket placeholders with values offered by the interactive client. To execute enumeration, replace `DRY` with `POLITE` or `AGGRESSIVE` after reviewing the commands.

Results default to `~/goscan`. To choose another output directory:

```text
set output_folder /path/to/results
```

## License

MIT. This project is based on [marco-lancini/goscan](https://github.com/marco-lancini/goscan). See `LICENSE` for the full terms and retained upstream copyright and permission notices.
