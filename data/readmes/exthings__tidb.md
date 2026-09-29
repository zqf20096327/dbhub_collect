# TiDB for Elixir

TiDB Vector Search and Ecto integration for Elixir applications.

Provides first-class vector data type support, Ecto custom types, vector distance query helpers, migration macros, and optional [Nx](https://github.com/elixir-nx/nx) tensor interop.

> [!WARNING]
> **Full-Text Search (FTS) Notice**: Full-Text Search (`FTS`) is currently **not supported** due to upstream TiDB limitations with parameterized non-constant query matching.

---

## Installation

Add `tidb` to your list of dependencies in `mix.exs`:

```elixir
def deps do
  [
    {:tidb, "~> 0.1.0"},
    # Optional dependencies
    {:nx, "~> 0.6", optional: true} # For Nx Tensor support
  ]
end
```

---

## Public API Reference

### 1. `TiDB.Vector`

Handles vector data structure manipulation, conversions, and serialization.

| Function | Description |
| :--- | :--- |
| `new(data)` | Creates a `%TiDB.Vector{}` from a `list`, `string`, `Nx.Tensor` (rank-1), or existing `%TiDB.Vector{}`. |
| `from_binary(binary)` | Reconstructs a `%TiDB.Vector{}` from a 32-bit float binary. |
| `to_binary(vector)` | Returns the underlying binary data (`vector.data`). |
| `from_string(string)` | Parses a vector from a TiDB JSON string literal (e.g. `"[1.0, 2.0]"`). |
| `to_list(vector)` | Converts a vector into a list of floats (rounded to 6 decimals). |
| `to_string(vector)` | Formats the vector as a TiDB SQL literal string (e.g. `"[1.0,2.0]"`). |
| `to_tensor(vector)` | *(Requires `:nx`)* Converts the vector into an `Nx.Tensor` with type `:f32`. |

### 2. `TiDB.Ecto.Vector`

An `Ecto.Type` implementation for mapping TiDB vector fields to `%TiDB.Vector{}` structs seamlessly.

```elixir
schema "documents" do
  field :embedding, TiDB.Ecto.Vector
end
```

### 3. `TiDB.Ecto.Vector.Query`

Macros for performing vector operations in Ecto queries:

| Macro | SQL Fragment | Description |
| :--- | :--- | :--- |
| `vec_cosine_distance(left, right)` | `VEC_COSINE_DISTANCE(?, ?)` | Calculates Cosine distance between vectors. |
| `vec_l2_distance(left, right)` | `VEC_L2_DISTANCE(?, ?)` | Calculates Euclidean (L2) distance. |
| `vec_l1_distance(left, right)` | `VEC_L1_DISTANCE(?, ?)` | Calculates Manhattan (L1) distance. |
| `vec_negative_inner_product(left, right)` | `VEC_NEGATIVE_INNER_PRODUCT(?, ?)` | Calculates negative inner product. |
| `vec_dims(vector)` | `VEC_DIMS(?)` | Returns the number of dimensions of a vector. |
| `vec_l2_norm(vector)` | `VEC_L2_NORM(?)` | Returns the L2 norm (magnitude) of a vector. |
| `vec_from_text(vector)` | `VEC_FROM_TEXT(?)` | Converts vector string into TiDB vector. |
| `vec_as_text(vector)` | `VEC_AS_TEXT(?)` | Formats vector to its text representation. |

### 4. `TiDB.Ecto.Migrations`

Migration helper macros for TiFlash replicas and vector indices:

| Macro | Description |
| :--- | :--- |
| `enable_tiflash(table, opts \\ [])` | Adds TiFlash replica (e.g., `replicas: 1`). |
| `disable_tiflash(table)` | Sets TiFlash replica to `0`. |
| `vector_index(table, column, opts \\ [])` | Creates a Vector index (`distance: :cosine | :l2`, `using: "HNSW"`, `name: "..."`). |
| `fulltext_index(table, column, opts \\ [])` | Creates a Full-Text index (`parser: :standard | :multilingual`, `name: "..."`). |

---

## Usage Example

### 1. Migration

```elixir
defmodule MyApp.Repo.Migrations.CreateDocuments do
  use Ecto.Migration
  import TiDB.Ecto.Migrations

  def up do
    create table(:documents) do
      add :title, :string
      add :content, :text
      add :embedding, :vector, size: 384
      timestamps()
    end

    # Enable TiFlash & Vector indexing (HNSW Cosine by default)
    enable_tiflash("documents")
    vector_index("documents", "embedding", distance: :cosine)
  end

  def down do
    drop table(:documents)
  end
end
```

### 2. Schema

```elixir
defmodule MyApp.Document do
  use Ecto.Schema
  import Ecto.Changeset

  schema "documents" do
    field :title, :string
    field :content, :string
    field :embedding, TiDB.Ecto.Vector

    timestamps()
  end

  def changeset(doc, attrs) do
    doc
    |> cast(attrs, [:title, :content, :embedding])
    |> validate_required([:title, :content, :embedding])
  end
end
```

### 3. Inserting Vectors

Vectors can be passed as raw number lists, `Nx` tensors, or `%TiDB.Vector{}` structs:

```elixir
# Using a list
%MyApp.Document{}
|> MyApp.Document.changeset(%{
  title: "Elixir Vector Search",
  content: "Fast semantic retrieval using TiDB",
  embedding: [0.023, -0.125, 0.891]
})
|> MyApp.Repo.insert!()

# Using TiDB.Vector explicitly
vec = TiDB.Vector.new([0.023, -0.125, 0.891])
MyApp.Repo.insert!(%MyApp.Document{title: "Doc 2", content: "...", embedding: vec})
```

### 4. Vector Similarity Search

```elixir
import Ecto.Query
import TiDB.Ecto.Vector.Query

query_embedding = TiDB.Vector.new([0.025, -0.120, 0.880])

# Find top 5 most similar documents using Cosine Distance
results =
  from(d in MyApp.Document,
    select: %{
      id: d.id,
      title: d.title,
      distance: vec_cosine_distance(d.embedding, ^query_embedding)
    },
    order_by: [asc: vec_cosine_distance(d.embedding, ^query_embedding)],
    limit: 5
  )
  |> MyApp.Repo.all()
```

---

## License

[Apache License 2.0](LICENSE)
