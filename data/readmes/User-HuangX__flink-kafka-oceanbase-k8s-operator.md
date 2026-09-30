# flink-kafka-oceanbase-k8s-operator

面向远程高吞吐数据接入的大数据处理服务骨架，当前按微服务边界拆成 3 个 Maven 模块：

| 模块 | 职责 | 默认端口 |
| --- | --- | --- |
| `tcp-ingress` | 远程 TCP 数据接入网关，接收数据并写入 Kafka 原始主题 | HTTP `8081` / TCP `9000` |
| `stream-processing` | 处理主调用链，消费 Kafka 原始主题，抽象处理后写入 OceanBase | 无固定 HTTP 端口 |
| `load-client` | 独立压测客户端，持续发送 RAW TCP 消息（默认 5 万条/秒） | 本地 CLI |

## 通信链路

当前不引入 RPC 框架。服务之间通过中间件和数据库边界解耦：

```text
Remote Producers
    -> tcp-ingress
    -> Kafka topic: remote-raw-data
    -> stream-processing
    -> OceanBase
```

如果后续确实需要同步服务调用，再单独引入 Dubbo，并把接口契约独立成 API 模块。

`stream-processing` 默认 `STREAM_FLINK_ENABLED=false`（本地配置）；在 Minikube 部署清单中显式设置为 `true`。

## 构建

```bash
mvn -DskipTests package
```

## 单模块启动

```bash
mvn -pl tcp-ingress spring-boot:run
mvn -pl stream-processing spring-boot:run
```

## 测试命令

```bash
# 全量测试
mvn test

# 仅某个模块（自动带依赖模块）
mvn -pl tcp-ingress -am test

# 单个测试类示例
mvn -pl tcp-ingress -Dtest=ProtocolHandlerSupportsTests test

# stream-processing 聚焦验证
mvn -pl stream-processing test
```

## 压测客户端（手动停止）

```bash
# 构建（纯 Go，零依赖，编译为静态二进制）
cd load-client-go && go build -o load-client .

# 运行
LOAD_HOST=$(minikube ip) LOAD_PORT=30900 LOAD_QPS=50000 LOAD_CONNECTIONS=20 \
./load-client-go/load-client
```

- 按 `Ctrl+C` 可手动停止。
- 交叉编译：`GOOS=linux GOARCH=amd64 go build -o load-client .`

## Minikube 一键部署与验证

```bash
# 部署（按顺序执行：打包 -> 构建镜像 -> 部署中间件 -> 建 topic -> 初始化 DB -> 部署业务）
scripts/minikube/deploy.sh

# 冒烟验证（发送 TCP 消息并检查 OceanBase）
scripts/minikube/smoke-test.sh

# 压测验证（当前发送 HTTP + MQTT，期望总数 = COUNT_PER_PROTOCOL * 2）
scripts/minikube/stress-test.sh
```

常用 NodePort：
- tcp-ingress TCP `30900`
- tcp-ingress HTTP `30081`
- Nacos `30848`
- OceanBase `30881`
- Sentinel `30858`

## 关键环境变量

| 变量 | 默认值 |
| --- | --- |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` |
| `KAFKA_RAW_TOPIC` | `remote-raw-data` |
| `OCEANBASE_URL` | `jdbc:mysql://localhost:2881/test` |
| `OCEANBASE_USERNAME` | `root` |
| `OCEANBASE_PASSWORD` | 空 |
| `TCP_INGRESS_PORT` | `9000` |
