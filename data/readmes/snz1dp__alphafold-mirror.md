# taiyiflow-alphafold · alphafold-mirror

> AlphaFold2/3 **Read-Through Cache 国内镜像站** —— 路径同构上游、懒加载、校验和验证、大文件断点续传、可离线交付。
> 与 `taiyiflow-mmseqs2`（序列检索）、`taiyiflow-esmfold`（结构预测）互补，本项目是**数据分发层**。

![AlphaFold 镜像下载中心](examples/snapshot.png)

> 下载中心总览页（`/af/`）：节点状态、文件清单、回源任务、客户端接入与合规声明入口。界面为中文，`go:embed` 内嵌于单二进制。

## 为什么需要

- AlphaFold2 全量遗传库 ~564 GB、AlphaFold3 数据库 ~239 GB，上游全部在境外（GCS/EBI/GWDG/wwPDB）。
- 国内直连 ~100 KB/s 量级且不稳定（`taiyiflow-mmseqs2` README 已实测记录）。
- 官方下载脚本把上游 URL 硬编码，但均为单一基址变量——**镜像保持路径同构即可一行 sed 接入**。

## 核心特性

| 特性 | 说明 |
|---|---|
| **路径同构** | 镜像 URL 与上游一一对应，客户端只改基址 |
| **懒加载** | 首次请求触发回源落盘，后续本地命中（sendfile 零拷贝） |
| **正确性** | 单飞防击穿 · 原子发布 · crc32c/md5/sha256 校验，绝不服务半截文件 |
| **大文件友好** | aria2c 多连接 · Range/206 · `curl -C -`/`wget -c` 断点续传 · 202+Retry-After |
| **滚动文件** | EBI/wwPDB TTL 再验证 + stale-while-revalidate，替换无 downtime |
| **离线交付** | 透明整文件布局，rsync 拷入内网 + `reindex` 重建元数据 |
| **合规** | AF3 权重默认 302 回源**永不落盘**；AF2 数据按许可镜像并署名 |

## 技术栈

**Go 单二进制**（控制面 + 数据面同进程，无 nginx）+ **aria2c** 回源子进程（os/exec 监管，崩溃自动重启）+ **PostgreSQL** 元数据（pgx/v5 纯 Go 驱动，内嵌迁移）。

> 技术栈分叉说明：兄弟项目（mmseqs2/esmfold）为 Python/FastAPI；本项目是纯 I/O 基础设施而非算法服务，Go 的高并发 I/O、零拷贝文件服务、单二进制交叉编译恰好命中需求。

## 快速开始

> **部署配置统一在 `BUILD.yaml`（snz1dpctl），不使用 docker-compose。** 镜像构建 `snz1dpctl make docker --push`；运行参数（端口/卷/环境变量/健康检查/路由）都在 `BUILD.yaml` 的 `service:` 段。

### 形态 A：单机（内网/有国际出口）

```bash
snz1dpctl make docker --push          # 构建并推送镜像
snz1dpctl make standalone             # 按 BUILD.yaml service 段起服务（PG 用平台实例）
# 服务 :8080，默认基路径 /af；启动自动迁移，目标库不存在时自动创建（需账号 CREATEDB 权限）
curl http://127.0.0.1:8080/af/health
```

> **对外地址**：内网默认 `http://afmirror:8080`（路径基址 `/af`）；公网部署可设 `https://<你的域名>/af`（自有域名，经前置网关/CDN 透传）。两个参数可单独配置（`BUILD.yaml` `service.envs` 或运行时 `-e` 覆盖）：
> - `AFMIRROR_BASE_PATH`：进程路由基路径，默认 `/af`（设空或 `/` 回到根路径）。
> - `AFMIRROR_PUBLIC_URL`：下载中心/文档/命令展示的对外基址，默认 `http://afmirror:8080`（内网）；公网设 `https://<你的域名>/af`。
>
> `BUILD.yaml` `service.ingress` 已配 `webroot: /af`、`strip-path: false`（保留前缀透传，与进程内 StripPrefix 等效）；根路径请求会 302 到基路径。公网经网关把 `https://<你的域名>/af/*` 路由到本服务。

### 形态 B：公网双节点（推荐）

国内 origin + 境外 fetcher（HK/SG），各自对接平台 PG，跨节点只走 HTTP dispatch/ingest。两台机器分别以 `AFMIRROR_ROLE=origin` / `AFMIRROR_ROLE=fetcher` 部署同一镜像，并注入 `AFMIRROR_FETCHER_URL`/`AFMIRROR_FETCHER_TOKEN`/`AFMIRROR_INGEST_TOKEN`（同一 SPLIT_TOKEN）：

```bash
# 境外 fetcher：AFMIRROR_ROLE=fetcher，FETCHER_URL 指向国内 origin
# 国内 origin：AFMIRROR_ROLE=origin，FETCHER_URL 指向境外 fetcher
# 令牌经 BUILD.yaml service.envs 或部署平台注入，勿落明文
```

### 形态 C：离线导入（气隙内网）

```bash
bash scripts/export_cache.sh /tmp/export        # 有网机导出
rsync -a /tmp/export/cache/ 内网机:/data/cache/  # 拷贝
AFMIRROR_UPSTREAM_DISABLED=true afmirror reindex # 内网重建
AFMIRROR_UPSTREAM_DISABLED=true afmirror serve   # 只读服务
```

## 客户端接入

```bash
# 默认基址 http://127.0.0.1:8080/af（本地）；公网用 AFMIRROR_BASE_URL=https://<你的域名>/af
# AF3 数据库（镜像感知脚本：202 轮询 + 校验 + zstd 解压 + READY 幂等）
bash scripts/download_af3_data.sh /data/af3

# AF2 数据库（full / reduced）
bash scripts/download_af2_data.sh /data/af2 reduced

# mmseqs2 / ColabFold 对接（download_databases.sh 来自 mmseqs2 项目，DB_BASE_URL 指向本镜像）
DB_BASE_URL=http://127.0.0.1:8080/af/colabfold ./scripts/download_databases.sh ./databases
```

详见 [examples/client_usage.md](examples/client_usage.md)。

## URL 映射（白名单制，未知路径 404）

| 镜像路径 | 上游 |
|---|---|
| `/alphafold-databases/<obj>` | GCS alphafold-databases（AF2 v2.3/casp14/reduced + AF3 v3.0） |
| `/alphafold/<obj>` | GCS alphafold（AF2 params） |
| `/alphafold3/<obj>` | GCS alphafold3（**restricted**，默认 302 回源） |
| `/ebi/<path>` | ftp.ebi.ac.uk/pub（UniRef90/UniProt 滚动） |
| `/gwdg/<path>` | wwwuser.gwdg.de/~compbiol（PDB70） |
| `/wwpdb/<path>` | files.wwpdb.org/pub（seqres/obsolete/CCD 滚动） |
| `/colabfold/<file>` | opendata.mmseqs.org/colabfold（需启用开关） |

## API

| 方法 | 路径 | 鉴权 | 说明 |
|---|---|---|---|
| GET | `/health` | 公开 | PG/aria2c/磁盘探活 |
| GET | `/v1/manifest` | 公开 | 全量清单 + 实时缓存状态 |
| GET | `/v1/cache` `/v1/cache/<key>/sha256` | 公开 | 缓存对象 / 校验和 |
| GET | `/v1/stats` `/v1/jobs` | 公开 | 命中率 / 任务进度 |
| POST | `/v1/prefetch` | admin | 预热 profile 或 key 列表 |
| POST/DELETE | `/v1/pin/<key>` | admin | 固定/解除固定 |
| DELETE | `/v1/cache/<key>` `/v1/jobs/<id>` | admin | 淘汰 / 取消 |
| GET | `/v1/licenses` | 公开 | 署名与许可（含中文合规声明 notice） |
| GET | `/licenses` | 公开 | 合规声明页（科研/非商业声明 + 上游署名 + 权重条款 + 免责） |
| GET | `/docs` `/openapi.json` `/metrics` | 公开 | API 文档 / Prometheus |

交互文档：`http://<host>:8080/af/docs`（公网 `https://<你的域名>/af/docs`）。

下载中心（`/af/`）与合规声明页（`/af/licenses`）为中文界面，`go:embed` 内嵌于单二进制（`internal/server/web/`）。下载中心首屏即展示**科研与社区非商业用途声明**横幅；受限权重（AF3）的下载命令须先在条款弹窗中勾选确认后才可复制。文件清单工具栏提供**缓存预热**入口（按 profile 组合或当前筛选批量回源，行级亦可单对象预热），须输入管理密钥（`ADMIN_TOKEN`）验证后才可提交；受限权重按合规红线拒绝预热。

## 合规（硬约束）

- **AF3 权重**：非商业 + 禁止组织外分享 + Google 机密。公开站**永不落盘**，默认 `redirect`（302 回 Google 直链）或 `deny`（403+条款）。`internal` 模式仅限单一非商业组织内网（鉴权+承诺）。
- **AF2 params**：CC BY 4.0（现行官方，tar 内 LICENSE 原样透传）。
- **BFD/UniRef30**：CC BY-SA 4.0（保持未修改）。**MGnify/PDB/Rfam/RNAcentral**：CC0。**UniProt**：CC BY 4.0。**NT RNA**：NCBI 公共领域政策。
- 许可核实记录与官方出处：[plans/licenses.md](plans/licenses.md)。
- **站点声明**：下载中心与 `/licenses` 页明确本站为非官方社区公益镜像，仅供科研/教学/社区非商业用途，不主张数据权利、与上游无隶属或背书关系，含免责声明与侵权处理（Notice & Takedown）渠道。

### internal 权重模式（仅限已授权组织内网）

仅当你已代表组织接受 [AF3 权重条款](https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md)（非商业、仅组织内部使用、不得组织外再分发）时才可启用。启用后权重**只在本组织内网节点落盘缓存**，内网即视为已授权，**无需 admin token**（省带宽、用户不必每次回 Google 拉取）：

```bash
AFMIRROR_WEIGHTS_POLICY=internal \
afmirror serve
# 首次 GET 触发回源（202 轮询），之后 HIT，无需任何令牌：
curl -O http://<内网基址>:8080/af/alphafold3/af3.bin.zst
```

边界（代码强制，不可绕过）：
- 内网免 token 直接放行落盘；`ADMIN_TOKEN` 仅用于管理接口（预热/淘汰/固定），与权重门控无关。
- 权重**不进任何预热 profile**、`/v1/prefetch` 显式 key 也拒绝（403）。
- 形态 B 下权重**绝不跨节点 dispatch/ingest**，只在发起请求的本节点本地回源。
- 默认 `redirect`/`deny` 行为完全不变；**公网部署切勿设为 `internal`**（权重永不公开落盘）。

## 开源与责任声明

**开发 / 开源方**：长沙慧码至一信息科技有限公司（太乙智启平台）。

**代码许可：[MIT License](LICENSE)**（Copyright © 2026 长沙慧码至一信息科技有限公司）。本仓库的**源代码及随附文档**采用 MIT 许可，可自由使用、复制、修改、合并、发布、分发、再授权与出售，唯须保留版权与许可声明，且软件按"现状"提供、不作任何担保。

> ⚠️ **MIT 仅覆盖代码，不覆盖数据。** 本软件缓存/分发的全部第三方数据（AlphaFold2/3 数据库与权重、BFD、UniRef、UniProt、PDB、Rfam、RNAcentral、NT RNA、ColabFold 库等）**不在 MIT 授权范围内**，仍按各自上游许可使用并署名（见上文「合规」章节与 `/licenses` 页）；AF3 权重另受 Google 非商业、禁止组织外分享条款约束，MIT 不构成对其再授权。

本项目由长沙慧码至一信息科技有限公司**以开源形式发布**，仅供学习、科研与技术交流。请在使用前务必知悉以下责任边界：

- **我们只开源代码，不部署、不运营任何镜像站点。** 本仓库提供的是软件源代码与构建/部署说明；任何实际运行的镜像节点均由**部署方自行搭建、自行运营、自行负责**。开源方不提供托管服务，也不对任何第三方部署的站点内容、可用性或其行为负责。
- **软件按"现状"（AS IS）提供，不作任何担保。** 在法律允许的最大范围内，开源方不对本软件的准确性、完整性、时效性、适销性或特定用途适用性作任何明示或暗示的担保，亦不对因使用或无法使用本软件而产生的任何直接、间接、附带、特殊或后果性损失承担责任。
- **数据与许可合规由部署方与使用者自行承担。** 本软件缓存/分发的全部数据版权归上游机构（Google DeepMind、EMBL-EBI、wwPDB、UniProt、NCBI、GWDG、ColabFold 等）所有，须按各自上游许可使用并署名。**部署方有义务确保其部署行为及数据用途符合上游许可与所在地法律法规**（尤其是 AF3 权重的非商业、禁止组织外分享条款）；因部署、运营或使用引发的任何许可纠纷、侵权或违法责任，由部署方/使用者自行承担，与开源方无关。
- **与上游无隶属或背书关系。** 本项目为非官方社区工具，与上述上游机构无任何隶属、合作、授权或背书关系；"AlphaFold" 等商标归各自所有者。
- **侵权处理（Notice & Takedown）**：若权利人认为某部署站点的内容侵犯其合法权益，请直接联系该**站点的部署方**处理；涉及本开源代码本身的问题，可通过项目仓库 Issue 反馈。

> 简言之：**代码开源、责任自负**。我们提供工具，不替你部署，也不为任何部署站点的合规性背书。下载中心与 `/licenses` 页中的"部署方"即指实际搭建并运营该镜像节点的组织或个人。

## 环境变量（全部 `AFMIRROR_` 前缀）

| 变量 | 默认 | 说明 |
|---|---|---|
| `ROLE` | standalone | standalone / origin / fetcher |
| `DATA_DIR` | /data | cache/staging/meta 根 |
| `PORT` | 8080 | HTTP 端口（数据面+控制面） |
| `BASE_PATH` | /af | 路由基路径（空或 `/` = 根路径） |
| `PUBLIC_URL` | http://afmirror:8080 | 对外展示/生成命令的基址（内网默认；公网可设 https://<你的域名>/af） |
| `DATABASE_URL` | postgres://afmirror:afmirror@postgres:5432/afmirror | PG DSN（目标库不存在时启动自动创建，需账号 CREATEDB 权限；无权限则报错提示手动建库） |
| `WEIGHTS_POLICY` | redirect | redirect / deny / internal（internal 仅限已授权组织内网，内网即授权、免 token 落盘缓存） |
| `MAX_CONCURRENT_FETCHES` | 2 | 全局回源并发 |
| `ARIA2_CONNECTIONS` | 8 | 单文件回源连接数 |
| `ARIA2_PORT` | 6800 | aria2 RPC 端口 |
| `UPSTREAM_PROXY` | 空 | 回源 HTTP 代理 |
| `TTL_MUTABLE_HOURS` | 168 | 滚动文件再验证周期 |
| `DISK_HIGH` / `DISK_LOW` | 85 / 75 | LRU 水位（%） |
| `ADMIN_TOKEN` | 空（禁用管理） | 管理鉴权（BUILD.yaml 部署默认 `snz1dp9527`，公网部署务必覆盖为强随机值） |
| `FETCHER_URL` / `FETCHER_TOKEN` | 空 | 形态 B origin 派单 |
| `INGEST_TOKEN` | 空 | 形态 B 接收鉴权 |
| `ENABLE_COLABFOLD` | false | ColabFold 命名空间（BUILD.yaml 部署默认 true；关闭时 `/colabfold/*` 一律 404） |
| `UPSTREAM_DISABLED` | false | 离线只读模式 |

## 构建

```bash
# 本地
CGO_ENABLED=0 go build -ldflags="-s -w" -o afmirror ./cmd/afmirror

# 镜像（amd64+arm64）；基础镜像默认走国内 DaoCloud 加速源（Dockerfile ARG REGISTRY_MIRROR）
snz1dpctl make docker --push
# 海外构建机/源失效时切回官方源：docker buildx build --build-arg REGISTRY_MIRROR=docker.io ...
# 备用国内源：--build-arg REGISTRY_MIRROR=docker.1ms.run（公共加速源可用性会变化，失效换源即可）

# 测试（PG 集成测试需 AFMIRROR_TEST_DSN）
AFMIRROR_TEST_DSN=postgres://afmirror:afmirror@127.0.0.1:5432/afmirror_test?sslmode=disable go test ./...

# 冒烟
AFMIRROR_BASE_URL=http://127.0.0.1:8080/af bash scripts/smoke_test.sh
```

## 目录结构

```
cmd/afmirror/        入口（serve/reindex/version）
internal/
  config/            AFMIRROR_* 环境变量
  server/            HTTP 数据面+控制面+中间件+OpenAPI+下载中心
  cache/             状态机+单飞+原子发布+LRU+统计聚合+reindex
  fetcher/           aria2c 监管 + JSON-RPC 客户端
  upstream/          白名单映射 + HEAD 探测 + 校验和
  manifest/          清单加载/profile 展开
  store/             PostgreSQL（pgxpool）+ 内嵌迁移
  policy/            权重门控
  server/migrations/ 三表 SQL（objects/jobs/stats + extra JSONB 扩展位）
manifests/           af2-v2.3.2 / af3-v3.0.5 / colabfold 清单
scripts/             gen_manifest.py + 下载/导出/冒烟脚本
plans/               设计文档 + 实施计划 + 许可核实 + 上游快照
```

## 已知限制

- `http.ServeContent` 仅支持**单 Range**；multipart/byteranges 降级 200 全量（aria2c/curl -C - 均为多个单 Range 连接，不受影响）。
- AF2 `pdb_mmcif` 为 2022-09-28 快照（官方走 rsync，HTTP 镜像用 AF3 tar 快照替代）；需要 live PDB 走官方 rsync。
- HTTPS 下 sendfile 退化为用户态拷贝；形态 B 由前置 LB/CDN 终结 TLS，origin 内网 HTTP 仍走 sendfile。

## 参考

- 设计：[plans/001-design.md](plans/001-design.md) · 实施：[plans/002-implementation.md](plans/002-implementation.md)
- 上游：AlphaFold2 v2.3.2 / AlphaFold3 v3.0.5 官方脚本（快照见 `plans/upstream-snapshots/`）
- 工程约定参考：`../taiyiflow-mmseqs2`