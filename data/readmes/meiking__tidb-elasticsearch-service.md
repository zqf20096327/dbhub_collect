# TiDB-ES Compatible Search Service
A lightweight Elasticsearch (ES)-compatible service that bridges TiDB with ES-style API requests. Supports dbname.tablename.indexname format for resource identification, with SQL-style backtick escaping for special characters.

## Core Specifications
Three-Segment Format (dbname.tablename.indexname)
* dbname: required
* tablename: required
* indexname: optional

### Format Rules
* Separator: . (dots in backticks are literal)
* Special chars (., !, , #): Wrap segment in `
* Valid examples:
    * simple_db.simple_tb
    * `db.with.dots`.`tb!123`
    * `db.name`.`tb!@#`.idx456

## ES API
* Endpoint: POST /{index}/_search
* Headers: Content-Type: application/json, Authorization: Basic Auth
* Request Body: ES Query DSL (core features: filter, sort, pagination)

**Example Request**
```
{
  "query": {"term": {"platform": 16}},
  "sort": [{"ts": "desc"}],
  "size": 5
}
```

**Example Response**
```
{
  "took": 15,
  "timed_out": false,
  "hits": {
    "total": {"value": 42},
    "hits": [{"_source": {"id": 1, "platform": 16, "ts": "2025-10-19T00:00:00Z"}}]
  },
  "_shards": {"total": 1, "successful": 1, "failed": 0}
}
```


# Quick Start
```
# Clone repo
git clone https://github.com/your-org/tidb-es-service.git
cd tidb-es-service

# Build
make build

# Usage
Usage of ./bin/tidb-es-service:
      --cache-salt string                  Required: Salt for generating cache key (use a long random string)
      --http-port string                   HTTP server port (e.g., :8080) (default ":8080")
      --tidb-conn-max-idle-time duration   TiDB connection max idle time (default 30m0s)
      --tidb-conn-max-lifetime duration    TiDB connection max lifetime (default 1h0m0s)
      --tidb-host string                   TiDB server address (host:port) (default "127.0.0.1:4000")
      --tidb-max-idle-conns int            TiDB max idle connections per (user+password+dbname) (default 10)
      --tidb-max-open-conns int            TiDB max open connections per (user+password+dbname) (default 20)
```

## Healthz
```
curl http://localhost:8080/healthz
```

## Metrics
```
curl http://localhost:8080/metrics
```

## Search Samples
- go: sampels/go/
- java: samples/java/
- python: samples/python/
