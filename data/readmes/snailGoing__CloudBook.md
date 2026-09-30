# Cloud Bookshelf v7

Cloud Bookshelf v7 is a sharded bookshelf synchronization service. The local
stack runs two MySQL 8 clusters, Redis 7, a single-node Kafka KRaft broker, the
HTTP API, the schema migrator, and the transactional Outbox relay.

## 多设备单账号云同步演示

下图和循环演示由仓库内嵌 Web 验证台的真实操作生成：设备 A 新增图书并上传，设备 B 拉取后修改阅读进度，设备 A 再拉取进度并发起删除，最终两端同步为空书架。

![CloudBook 双设备阅读进度同步](docs/assets/cloudbook-multi-device-demo.png)

![CloudBook 多设备单账号云同步完整演示](docs/assets/cloudbook-multi-device-demo.gif)

[播放 MP4 演示](docs/assets/cloudbook-multi-device-demo.mp4) · [查看技术方案与架构设计](docs/architecture.md) · [系统化学习业务类图、模块关系与程序流程](docs/business-architecture-guide.md)

## Local Setup

Local development requires Go 1.23, Docker Compose, `curl`, and `jq`. Install
`k6` only when running the optional load workflow.

Start by creating the local environment file:

```bash
cp .env.example .env
```

The example contains development-only credentials and enables
`DEV_TRUSTED_HEADERS=true`. In this mode the API trusts `X-User-ID` and
`X-Device-ID`; deploy behind an authenticated gateway and disable trusted
headers outside local development.

Build the Go binaries and application images, then start the stack:

```bash
make build
docker compose -f deploy/compose.yaml build
docker compose -f deploy/compose.yaml up -d
docker compose -f deploy/compose.yaml ps
curl --fail http://127.0.0.1:8080/health/ready
curl --fail http://127.0.0.1:8081/health/ready
```

The Compose `migrate` service runs before API and Relay startup. Migration is
idempotent; this command can be run twice to verify that property:

```bash
docker compose -f deploy/compose.yaml run --rm migrate
docker compose -f deploy/compose.yaml run --rm migrate
```

To run the migrator directly from the host, export the host DSNs first:

```bash
export MYSQL_CLUSTER_0_DSN='bookshelf:bookshelf-local-app@tcp(127.0.0.1:33060)/bookshelf'
export MYSQL_CLUSTER_1_DSN='bookshelf:bookshelf-local-app@tcp(127.0.0.1:33061)/bookshelf'
make migrate
```

Stop only this Compose project without deleting its named volumes:

```bash
docker compose -f deploy/compose.yaml down
```

## API Examples

The first pull lazily creates the account clock and returns a decimal
`cache_ver` string:

```bash
curl --fail --get 'http://127.0.0.1:8080/api/v1/shelf/list' \
  -H 'X-User-ID: 1001' \
  -H 'X-Device-ID: 00000000-0000-4000-8000-000000000001' \
  --data-urlencode 'page=1' \
  --data-urlencode 'limit=200'
```

Upload an ADD using that version:

```bash
now_ms=$(($(date +%s) * 1000))
curl --fail 'http://127.0.0.1:8080/api/v1/shelf/update?cache_ver=0' \
  -H 'Content-Type: application/json' \
  -H 'X-User-ID: 1001' \
  -H 'X-Device-ID: 00000000-0000-4000-8000-000000000001' \
  --data "{\"device_id\":\"00000000-0000-4000-8000-000000000001\",\"client_now_ms\":$now_ms,\"items\":[{\"op_id\":\"00000000-0000-4000-8000-000000000101\",\"book_id\":\"42\",\"type\":\"ADD\",\"changed_at_ms\":$now_ms,\"book_name\":\"The Left Hand of Darkness\",\"author\":\"Ursula K. Le Guin\"}]}"
```

Pull a DELTA from a known version:

```bash
curl --fail --get 'http://127.0.0.1:8080/api/v1/shelf/list' \
  -H 'X-User-ID: 1001' \
  -H 'X-Device-ID: 00000000-0000-4000-8000-000000000001' \
  --data-urlencode 'page=1' \
  --data-urlencode 'limit=200' \
  --data-urlencode 'cache_ver=0'
```

For a multi-page response, use only the returned `sync_id` and `next_page` on
subsequent requests. `cache_ver` appears only on the final page.

## 双设备 Web 同步验证台

本地 Compose 环境默认启用内嵌验证台。用两个浏览器标签页打开同一账号，分别模拟 A、B 两台设备：

```text
http://127.0.0.1:8080/demo?device=A&user_id=1001
http://127.0.0.1:8080/demo?device=B&user_id=1001
```

先在 A 设备新增书籍并同步，再到 B 设备同步以查看新增结果；随后可在 B 设备修改阅读进度并同步，回到 A 设备同步检查进度。删除操作也采用相同步骤验证。移动端页面支持下拉触发同步，桌面端和移动端都可以使用“立即同步”按钮。

验证台通过 `X-User-ID` 和 `X-Device-ID` 请求头直接调用同源 API，仅用于本地开发或受控测试环境。生产部署必须设置 `DEMO_UI_ENABLED=false`，并同时关闭 `DEV_TRUSTED_HEADERS`。

## Verification

Run the complete local verification matrix from the repository root:

```bash
gofmt -w cmd internal tests
go test ./...
go test -race ./...
go test -tags=integration ./...
go vet ./...
docker compose -f deploy/compose.yaml config
make test-integration
make smoke
```

Integration tests use the real Compose dependencies through local-only ports.
The defaults can be overridden with `BOOKSHELF_BASE_URL`,
`MYSQL_CLUSTER_0_TEST_DSN`, `MYSQL_CLUSTER_1_TEST_DSN`, `REDIS_TEST_ADDR`, and
`KAFKA_TEST_BROKERS`. Tests create unique user, device, and event identifiers
and remove only rows and Redis data they own. Failure tests pause shared
services serially and always restore them during cleanup.

Run the intended public pull-path benchmark:

```bash
go test -tags=integration ./tests/integration -run '^$' -bench BenchmarkPublicPullSinglePage -benchtime=2s
```

Run the k6 workload with a local k6 installation. Load users default to the
high, JavaScript-safe range beginning at `9000000000000`, avoiding state left
by examples or smoke tests. Override `USER_ID_BASE` with another positive safe
integer when a clean namespace is needed:

```bash
BASE_URL=http://127.0.0.1:8080 \
RELAY_METRICS_URL=http://127.0.0.1:8081/metrics \
USER_ID_BASE=9000000000000 \
PULL_VUS=4 UPLOAD_VUS=4 CONFLICT_VUS=8 CONFLICT_USERS=1 \
DURATION=2m METRICS_EVERY=5 \
k6 run --summary-export=load-summary.json scripts/load.js
```

The three scenarios exercise single-page pulls, per-user ADD/progress/remove
uploads, and multi-device uploads against shared users. Expected
`CACHE_VER_STALE` and `SYNC_BUSY` responses in the conflict scenario are
reported separately and do not count as failed HTTP requests. The k6 summary
includes `bookshelf_load_operations_total`, applied/stale/busy upload totals,
unexpected-response rate, and current PENDING/PROCESSING/DEAD Outbox rows plus
the oldest backlog age. Each user reuses one book, so a long run does not turn
into an accidental pagination test.

Measure SQL amplification from real MySQL statement counters. Immediately
before the k6 run, reset the digest counters on both local clusters:

```bash
docker compose -f deploy/compose.yaml exec -T mysql-00 sh -lc \
  'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "TRUNCATE TABLE performance_schema.events_statements_summary_by_digest"'
docker compose -f deploy/compose.yaml exec -T mysql-01 sh -lc \
  'mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e "TRUNCATE TABLE performance_schema.events_statements_summary_by_digest"'
```

After the run, collect the executed statement count from each cluster:

```bash
docker compose -f deploy/compose.yaml exec -T mysql-00 sh -lc \
  'mysql -N -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SELECT COALESCE(SUM(COUNT_STAR),0) FROM performance_schema.events_statements_summary_by_digest WHERE SCHEMA_NAME=\"bookshelf\""'
docker compose -f deploy/compose.yaml exec -T mysql-01 sh -lc \
  'mysql -N -uroot -p"$MYSQL_ROOT_PASSWORD" -e "SELECT COALESCE(SUM(COUNT_STAR),0) FROM performance_schema.events_statements_summary_by_digest WHERE SCHEMA_NAME=\"bookshelf\""'
```

SQL amplification is the sum of those two counts divided by the k6
`bookshelf_load_operations_total` count. The total intentionally includes
Relay and readiness/metrics traffic that reached MySQL during the measured
window; keep probe frequency and `METRICS_EVERY` fixed when comparing runs.

Inspect application conflict and durable backlog metrics directly when
investigating a run:

```bash
curl --silent http://127.0.0.1:8080/metrics | \
  awk '/^bookshelf_upload_(lock|version)_conflicts_total/'
curl --silent http://127.0.0.1:8081/metrics | \
  awk '/^bookshelf_outbox_(events|oldest_age_seconds|retries_total|dead_total)/'
```

The benchmark and k6 output report local API latency and throughput. Local
Docker results validate the workflow and functional behavior only; they do not
prove the PolarDB target of 35,000 SQL QPS per cluster.

## Operational Boundaries

MySQL is the source of truth for cache versions, sync locking, state, and
Outbox events. Redis stores only immutable five-minute pagination sessions.
Kafka is asynchronous: an upload succeeds after the MySQL state/version/Outbox
transaction commits, even while Kafka is unavailable. Relay publishes each
committed event to `bookshelf.state.changed.v1` and `bookshelf.audit.v1` with
at-least-once delivery, so consumers deduplicate by `event_id`.
