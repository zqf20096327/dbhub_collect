## Usage

> TiDB Vector is not released currently.

### Pre-requirements

Install TiDB Vector

```shell
$ pip install tidb-vector
```

Prepare your database info and create a `.env` file in working directory

```
TIDB_HOST=<your-cluster-host>
TIDB_USER=<your-cluster-user>
TIDB_PASSWORD=<your-cluster-password>
TIDB_PORT=4000
TIDB_DB_NAME=<your-database-name>
```

### Basic Usage

```python
from tidb_vector import VectorStore, VectorDocument

# Initialize a Vector Store
vc = VectorStore()

# Open or create a Vector Collection
c = vc.open_collection(name='a_cool_collection_name')

# Insert documents
c.insert([
    VectorDocument(
        document_id='id-0',
        vector=[1, 2, 4, 5, 6, 7],
        content='The raw content of the document',
        metadata={}
    )
])

# Similarity search
results = c.cosine_similarity(vector=[1, 2, 3, 4], limit=13)
for result in results:
    print(result.id, result.content, result.similarity)
```

