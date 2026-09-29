# rconceptnet

A simple Rust implementation of [ConceptNet](https://conceptnet.io) written explicitly with performance and ease of use in mind. ConceptNet's default tooling is written in Python and requires Postgres with significant resource requirements. This project uses an SQLite DB file instead.

> The original ConceptNet project seems to have stalled with no updates to its database since 2019. Despite that, it is still a highly valuable corpus.

Download the pre-compiled binary from the [releases](https://github.com/knadh/rconceptnet/releases) page.

## Import

Check out the latest [ConceptNet files](https://github.com/commonsense/conceptnet5/wiki/Downloads).

```sh
# Download the latest file (about ~500 MB).
curl -O --progress-bar https://s3.amazonaws.com/conceptnet/downloads/2019/edges/conceptnet-assertions-5.7.0.csv.gz

# Import (only 'en' English. Specify one or more --lang, or no --lang at all to import everything)
rconceptnet import --db conceptnet.db --lang en conceptnet-assertions-5.7.0.csv.gz

```

## Query

### CLI

```sh
rconceptnet query bamboo
rconceptnet query "play game" --relation IsA
rconceptnet query bamboo --tree
rconceptnet query bamboo --json
rconceptnet query bamboo -n 10 -l en -r PartOf
```

## Server

Run a JSON query webserver.

```sh
rconceptnet serve --port 3000
```

### HTTP API

```
GET http://localhost:3000/?query=bamboo&lang=en&relation=IsA&limit=30
```

| Param      | Default | Description                               |
| ---------- | ------- | ----------------------------------------- |
| `query`    | -       | Concept/word to look up (required)        |
| `lang`     | `en`    | ConceptNet language code                  |
| `relation` | -       | Filter by relation (e.g: `IsA`, `PartOf`) |
| `limit`    | `30`    | Max results                               |

Returns a JSON array of results.

```json
[
  {
    "relation": "IsA",
    "relation_uri": "/r/IsA",
    "start_label": "bamboo",
    "start_uri": "/c/en/bamboo",
    "end_label": "wood",
    "end_uri": "/c/en/wood",
    "weight": 2.0,
    "surface_text": "bamboo is a type of wood"
  }
]
```

Licensed under the MIT License.
