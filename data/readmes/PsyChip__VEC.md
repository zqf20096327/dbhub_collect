# VEC

VEC is a compact, exact-scan vector database. `vec` keeps vectors on an NVIDIA
GPU; `vec-cpu` uses system RAM and implements the same wire commands.

```bash
# GPU, fp32, TCP port 1920 plus the local pipe/socket
vec tools 1024

# GPU, fp16 storage
vec tools 1024:f16

# CPU, fp32 only
vec-cpu tools 1024

# Empty writable database for this process only; no persistence files are read or written
vec --memory tools 1024
vec-cpu --memory tools 1024
```

Records have a stable integer slot ID, an optional label, and an optional opaque
data blob. The minimal external-database workflow is still supported:

```python
from sdk.vec_client import VecClient

db = VecClient("tools")
index = db.push(embedding)       # vector in -> integer ID out
records = db.get(index)          # pull it back by ID
hits = db.query(other_embedding) # nearest IDs plus requested fields
```

Use shape `0` when the external database owns all metadata: QUERY/QID return
only index and squared-L2/cosine distance, and GET returns only index.

## SDKs and transport

The supplied SDKs connect directly to a local database name:

| OS | Local endpoint |
|---|---|
| Windows | `\\.\pipe\vec_<name>` |
| Linux | `/tmp/vec_<name>.sock` |

| SDK | File |
|---|---|
| C++ (header-only) | [`sdk/vec_client.h`](sdk/vec_client.h) |
| Python 3 + NumPy | [`sdk/vec_client.py`](sdk/vec_client.py) |
| Node.js | [`sdk/vec_client.js`](sdk/vec_client.js) |
| TypeScript declarations | [`sdk/vec_client.d.ts`](sdk/vec_client.d.ts) |
| Delphi | [`sdk/vec_client.pas`](sdk/vec_client.pas) |

The server also accepts the binary protocol over TCP (default port `1920`) and
has deploy/router modes. Those remote/router transports are not exposed by the
current SDK APIs. There is no text command interface.

See the [SDK guide](sdk/README.md), [endpoint datasheet](sdk/DATASHEET.md), and
[wire protocol](sdk/PROTOCOL-2.0.md).

## Commands

- `PUSH` stores a vector and returns its integer slot ID. Inline data is optional
  but requires a label.
- `QUERY` searches by a supplied vector; `QID` searches by a stored ID or label.
- `EXISTS` performs exact stored-representation lookup.
- `GET` fetches records by ID, label, or ID batch.
- `UPDATE` changes only a vector; `LABEL`, `SET_DATA`, and `GET_DATA` manage
  sidecars.
- `DELETE` tombstones a slot; `UNDO` removes the last physical slot.
- `CLUSTER`, `DISTINCT`, and `REPRESENT` provide DBSCAN, farthest-point sampling,
  and one farthest-from-centroid member per cluster.
- `INFO` returns database metadata; `SAVE` persists dirty state in normal mode
  and is an acknowledged no-op in `--memory` mode.

QUERY/QID/GET use a shape mask: `0x01` vector, `0x02` label, `0x04` data.
The SDK default is `0x07`; `0x00` is useful when only IDs/distances are needed.
L2 distances are squared Euclidean distances. GPU QUERY/QID return at most 16
records. CPU defaults to 50 and accepts `--topk=N` for `1..100`.

PUSH rejects an exact duplicate of an alive vector. In fp16 databases, exactness
is evaluated after conversion to the stored fp16 representation. UPDATE does not
run this duplicate check.

## Persistence

For `vec tools 1024`, the files are based on `tools_1024_f32`:

```text
.tensors  [dim][count][deleted][fmt][one-byte alive flags][vectors][CRC32]
.meta     [count][per-slot label length + bytes]
.hashes   [count][per-slot xxh64][CRC32]
.data     [count][one-byte presence flags][packed blobs][CRC32]
```

`.tensors` is authoritative. Missing or invalid `.hashes` is rebuilt from it.
`.meta` is written only when at least one label exists; `.data` only when at
least one blob exists. The loaders do not validate `.meta` or `.data` with the
tensor CRC status. See the wire protocol for the exact layouts and caveats.

Dirty databases autosave after 60 seconds without a write. `SAVE` requests an
immediate save; clean, read-only, and empty databases can make it a no-op.

`--memory` starts a new empty database and disables all persistence I/O. It does
not discover or load existing files, autosave, or save on shutdown. `SAVE` is an
acknowledged no-op, and any existing files with the same database name remain
unchanged. Transport endpoints are unaffected.

## Build

`vec` requires the NVIDIA CUDA toolkit. `vec-cpu` requires a C++ compiler.

```bash
# Windows
build.bat

# Linux
./build.sh
```

Windows production executables are written to `dist\`. VEC links the CUDA
runtime statically, so `dist\cuda` is present for layout consistency but does
not contain redistributable DLLs.

The GPU build accepts SM 7.5, 8.0, 8.6, 8.9, 9.0, and 10.0. The CPU build is
fp32-only.

## Command-line reference

```bash
vec tools 1024 1921            # custom TCP port
vec --notcp tools 1024         # local pipe/socket only
vec --memory tools 1024        # empty database; no persistence reads or writes
vec deploy                     # discover and launch databases
vec --route 1920               # route namespaced frames
vec tools --check              # inspect the matching .tensors file
vec tools --repair             # repair the matching .tensors file
vec tools --delete             # delete matching .tensors and .meta files
vec --help

vec-cpu tools 1024 --topk=100
vec-cpu --memory tools 1024
```

`--check`/`--repair` operate on tensor files. As currently implemented,
`--delete` removes matching `.tensors` and `.meta` files, but not `.hashes` or
`.data` sidecars.

---

*Created by [@PsyChip](mailto:root@psychip.net) — June 2026*
