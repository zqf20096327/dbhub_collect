# tikv-setup

A utility for creating customized, rootless TiKV and Placement Driver (PD) container images. This project builds "lean" images compiled from source, packaged on a modern openSUSE base without unnecessary runtime bloat.

Base Image: openSUSE Leap 16.0 (Runtime) / Leap 15.6 (Build)
TiKV/PD Version: 8.5.5 (Official Source Release)

## Pre-requisites

OS: Linux-based.

<table>
    <caption>Required Tools</caption>
    <thead>
        <tr>
            <th>Package</th>
            <th>Version</th>
            <th>Notes</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Python</td>
            <td>3.13+</td>
            <td>
                <p>Core language the CLI tool is written in.</p>
            </td>
        </tr>
        <tr>
            <td><a href="https://python-poetry.org/docs/">Poetry</a></td>
            <td>2.2.1+</td>
            <td>
                <p>Project dependency manager.</p>
            </td>
        </tr>
        <tr>
            <td><a href="https://buildah.io/">Buildah</a></td>
            <td>1.41.5+</td>
            <td>
                <p>Used to programmatically create OCI-compliant container images without a daemon.</p>
            </td>
        </tr>
        <tr>
            <td><a href="https://taskfile.dev/">Taskfile</a></td>
            <td>3.46.3+</td>
            <td>
                <p>Optional. You can use the provided <a href="taskw">shell script wrapper</a> (<code>./taskw</code>) which scopes the binary to the project.</p>
            </td>
        </tr>
    </tbody>
</table>

## Usage

List available tasks:

```shell
TASKFILE_BINARY="./taskw"

$TASKFILE_BINARY --list
```

Install dependencies:

```shell
TASKFILE_BINARY="./taskw"

$TASKFILE_BINARY deps
```

View CLI tool options and build help:

```shell
TASKFILE_BINARY="./taskw"

$TASKFILE_BINARY run -- --help
```

### Example

Build the core artifacts (downloads and compiles TiKV and PD from source):

```shell
TASKFILE_BINARY="./taskw"

$TASKFILE_BINARY run -- apps pd core build
$TASKFILE_BINARY run -- apps tikv core build
```

Build the runtime images (sets up users, copies binaries, and configures entrypoints):

```shell
TASKFILE_BINARY="./taskw"

$TASKFILE_BINARY run -- apps pd runtime build
$TASKFILE_BINARY run -- apps tikv runtime build
```

Run the built containers using Podman shell commands:

- Standalone Mode (Single node TiKV + PD cluster):

  1. PD Container:

  ```shell
  #!/bin/bash

  CONTAINER="tikv_pd"
  NETWORK="systemd-leap"
  NETWORK_ALIAS="pd"
  CONTAINER_UID=1001
  CONTAINER_GID=1001

  IMAGE="localhost/tikv-setup-pd-runtime:8.5.5"

  # Host path for persistent data
  HOST_DATA_DIR="/opt/container-data/tikv/pd/data"

  # Create network if it doesn't exist
  podman network exists $NETWORK || podman network create $NETWORK

  # Ensure host directory exists and permissions are set for the container user
  mkdir -p "$HOST_DATA_DIR"
  podman unshare chown -R $CONTAINER_UID:$CONTAINER_GID "$HOST_DATA_DIR"

  podman run -d \
    --name $CONTAINER \
    --network $NETWORK \
    --network-alias $NETWORK_ALIAS \
    --user $CONTAINER_UID:$CONTAINER_GID \
    -p 127.0.0.1:2379:2379 \
    -p 127.0.0.1:2380:2380 \
    -v "$HOST_DATA_DIR":/usr/local/pd/data:Z \
    $IMAGE \
    pd-server --config /usr/local/pd/conf/pd.toml
  ```

  2. TiKV Container:

  ```shell
  #!/bin/bash

  CONTAINER="tikv_tikv"
  NETWORK="systemd-leap"
  NETWORK_ALIAS="tikv"
  CONTAINER_UID=1001
  CONTAINER_GID=1001

  IMAGE="localhost/tikv-setup-tikv-runtime:8.5.5"

  # Host path for persistent data
  HOST_DATA_DIR="/opt/container-data/tikv/tikv/data"

  # Create network if it doesn't exist
  podman network exists $NETWORK || podman network create $NETWORK

  # Ensure host directory exists and permissions are set for the container user
  mkdir -p "$HOST_DATA_DIR"
  podman unshare chown -R $CONTAINER_UID:$CONTAINER_GID "$HOST_DATA_DIR"

  podman run -d \
    --name $CONTAINER \
    --network $NETWORK \
    --network-alias $NETWORK_ALIAS \
    --user $CONTAINER_UID:$CONTAINER_GID \
    -p 127.0.0.1:20160:20160 \
    -v "$HOST_DATA_DIR":/usr/local/tikv/data:Z \
    $IMAGE \
    tikv-server --config /usr/local/tikv/conf/tikv.toml
  ```

## Application Container Image Features

### Ports

<table> <thead> <th>Port</th> <th>Service</th> <th>Purpose</th> </thead> <tbody> <tr> <td><code>2379</code></td> <td><strong>PD</strong></td> <td><strong>Client Port.</strong> The main entry point for TiKV nodes and database clients (e.g., SurrealDB) to query cluster metadata.</td> </tr> <tr> <td><code>2380</code></td> <td><strong>PD</strong></td> <td><strong>Peer Port.</strong> Used exclusively for PD-to-PD communication and Raft consensus in multi-node setups.</td> </tr> <tr> <td><code>20160</code></td> <td><strong>TiKV</strong></td> <td><strong>gRPC Port.</strong> The primary data traffic port for key-value read/write operations between clients and the storage engine.</td> </tr> </tbody> </table>

### Volumes

<table> <thead> <th>Path</th> <th>Application</th> <th>Purpose</th> </thead> <tbody> <tr> <td><code>/usr/local/pd/data</code></td> <td><strong>PD</strong></td> <td>Stores the cluster metadata and leader election state (etcd). <strong>Critical:</strong> Must use the <code>:Z</code> SELinux flag if using host bind mounts on openSUSE.</td> </tr> <tr> <td><code>/usr/local/tikv/data</code></td> <td><strong>TiKV</strong></td> <td>Stores the actual RocksDB SST files and Raft logs. <strong>Critical:</strong> Must use the <code>:Z</code> SELinux flag if using host bind mounts on openSUSE.</td> </tr> </tbody> </table>

### Environment variables & Configuration

Configuration for both services is primarily handled via TOML files baked into the image at /usr/local/pd/conf/pd.toml and /usr/local/tikv/conf/tikv.toml.

However, the entrypoints allow you to pass CLI flags to override TOML settings at runtime.

<table> <thead> <th>Flag</th> <th>Target</th> <th>Example</th> <th>Purpose</th> </thead> <tbody> <tr> <td><code>--name</code></td> <td>PD</td> <td><code>--name pd-node-1</code></td> <td>Unique identifier for the PD server in the cluster.</td> </tr> <tr> <td><code>--advertise-client-urls</code></td> <td>PD</td> <td><code>--advertise-client-urls http://pd:2379</code></td> <td>The URL this PD node tells clients (and TiKV) to use to reach it. Important for proxy/Tailscale setups.</td> </tr> <tr> <td><code>--advertise-addr</code></td> <td>TiKV</td> <td><code>--advertise-addr tikv:20160</code></td> <td>The URL this TiKV node registers with PD so clients can locate it.</td> </tr> <tr> <td><code>--pd-endpoints</code></td> <td>TiKV</td> <td><code>--pd-endpoints http://pd:2379</code></td> <td>Tells the TiKV node where to find the Placement Driver on startup.</td> </tr> </tbody> </table>

Note: For single-node development, ensure max-replicas = 1 is set inside your custom pd.toml to disable noisy quorum warnings. For memory safety, bound TiKV by setting block-cache.capacity in tikv.toml.