# mssql-db-migration

把 SQL Server 的表结构与全量数据迁移到人大金仓 KingbaseES（PG 兼容模式）/ 达梦 DM8。
工具自身名、命令与 Maven 坐标仍叫 `dbsync`（`bin/dbsync`、`com.dbsync.*`），仓库名只用于对外发布。
引擎优先、纯 JDBC：方言差异收敛在 `Dialect` 接口（`KingbaseDialect` / `DmOracleDialect`），
新增国产目标库 = 新增一个 Dialect 实现 + 在 `DialectFactory` 注册，core 业务代码不改。

## 当前进度

已实现（里程碑 1 / MVP，端到端可用）：

- `schema` + `dialect`：结构翻译（建序列/建表/**非自增列默认值翻译**/索引/外键/序列重置），类型映射与告警报告；
  `Dialect`/`TypeMapper`/`DefaultTranslator` 抽象 + 金仓（PG 兼容）、达梦（DM8 Oracle 兼容）两个方言实现。
- `source`：`SqlServerSchemaReader` 读 SQL Server `dbo` 表/列/主键/索引/外键。
- `transfer`：`FullLoader` 单表全量搬运（流式读、分批提交、显式插主键、装载后重置序列）。
- `job`：`MigrationRunner` 端到端编排（建结构 → 逐表灌数 → 建索引/加外键），
  支持**多表并行 + 单表按主键值域分片**（`--parallel`/`--shards`，fail-fast 报出是在哪张表哪个分片失败）。
- `transfer` 写入策略可换：默认 `jdbc`（逐行批量，兼容所有驱动），`copy` 用反射调 PG 系驱动的
  `CopyManager` 走 `COPY ... FROM STDIN`（金仓高速加载，以 PG 驱动做替身验证）；提交阈值 = 行数或字节数。
- `verify`：逐表行数 + 校验和比对（默认全量，可选按主键值域分桶抽样），列级差异定位，JSON 报告。
- `state` + `reconcile` + `job`：增量补数（水位复合游标分页 + 按主键 upsert）、本地状态文件断点续跑、主键对账。
- `dbsync-cli`：`plan`（dry-run）、`full`（真跑）、`verify`（校验）、`sync`（增量）、`reconcile`（对账）、
  `encrypt-password`（口令加密）六个子命令 + YAML 配置（支持 `${env:...}` 与 `${enc:...}` 口令写法）；
  `plan --out` 可把 DDL 落盘，`full --recreate` 支持目标已有结构时 DROP 重建后重跑，
  `full` 失败自动写 `.dbsync-failed` 失败清单。
- `dbsync-gui`：桌面版（Swing，零第三方依赖，单 shaded jar）：同一个 YAML、同一套编排，
  配置/操作/日志三个页签，后台线程执行 + 尽力中断，全链路脱敏。
- `dbsync-dist`：离线发布物（启动脚本 + **切换门禁脚本** + 驱动放置点 + 示例配置 + 打包脚本），
  内网只装 JRE 即可跑。

尚未实现：达梦 `dmfldr` 外部进程加载；真实金仓实例/驱动的忠实性验证（当前目标库一律用 PG 容器替身）。

## 构建

```bash
mvn -q test                              # 容器测试需要 Docker，否则被跳过
mvn -pl dbsync-cli -am package
mvn -o -pl dbsync-gui -am package         # → dbsync-gui/target/dbsync-gui-<版本>-shaded.jar
mvn -o -pl dbsync-dist -am package        # 离线发布物：dbsync-dist/target/dist/
```

打包产物 `dbsync-cli/target/dbsync-cli-0.1.0-SNAPSHOT-shaded.jar` 内含 picocli、snakeyaml、
`dbsync-core` 与 SQL Server 驱动；**目标金仓驱动不内置**，运行时经 classpath 提供：

```bash
java -cp "dbsync-cli/target/dbsync-cli-0.1.0-SNAPSHOT-shaded.jar:/path/to/kingbase8.jar" \
     com.dbsync.cli.Dbsync full -c config.yaml
```

## 配置

口令支持三种写法：`${env:VAR}` 环境变量插值（推荐）、`${enc:v1:...}` 密文（由 `dbsync encrypt-password` 生成）、
明文（仅临时排障）：

```yaml
source:
  url: "jdbc:sqlserver://host:1433;databaseName=appdb;encrypt=false"
  user: sa
  password: "${env:DBSYNC_SRC_PWD}"
target:
  type: kingbase                        # kingbase | dm；driverClass 缺省按 type 推断
  url: "jdbc:kingbase8://host:54321/appdb"
  user: system
  password: "${env:DBSYNC_TGT_PWD}"
  # driverClass: org.postgresql.Driver  # 用 PG 容器做替身时覆盖
options:
  batchSize: 2000
  fetchSize: 5000
  maxBatchBytes: 8388608            # 单批字节估算上限（8 MiB），0 = 只按行数提交
  parallelThreads: 4                # 并行线程数，默认 1（串行）
  shards: 4                         # 单表主键值域分片数，默认 1；仅单列整数主键生效
  bulkLoad: jdbc                    # jdbc（默认）| copy（金仓高速加载，需 copyManagerClass）
  watermarkColumn: updated_at       # 默认水位列名（忽略大小写）
  watermarkLookbackSeconds: 5       # 安全回溯窗口，0 = 关闭（见「已知限制」）
  stateFile: .dbsync-state          # 相对「配置文件所在目录」；绝对路径原样使用
  maxKeys: 500000                   # pk-append / reconcile 的单表主键集合内存上限
tables:
  overrides:                        # 逐表增量覆盖（表名忽略大小写）
    code_table:
      incremental: { strategy: full-reload }
    attendance_record:
      incremental: { strategy: watermark, watermarkColumn: last_modified }
```

策略取值：`watermark`（默认，需水位列 + 主键）、`pk-append`（只补目标缺失的主键行，不发现更新）、
`full-reload`（truncate 后整表重灌，适合无主键小表）。`full-compare` 未实现，配置即报错；
配置里出现源库不存在的表名只告警（`TABLE_OVERRIDE_UNKNOWN`），不中断整轮。

## 用法

```bash
# dry-run：读源 + 翻译，打印将执行的 DDL 与全部告警，不连目标库
dbsync plan -c config.yaml
dbsync plan -c config.yaml --out ddl.sql                  # 同一份内容存成 .sql（可人工审阅/分批执行）

# 端到端全量迁移
dbsync full -c config.yaml
dbsync full -c config.yaml --parallel 4 --shards 4        # 多表并行 + 大表分片
dbsync full -c config.yaml --bulk-load copy               # 金仓 COPY 高速加载（类名见配置）
dbsync full -c config.yaml --failed-list /tmp/failed.txt  # 失败清单落盘位置（默认配置同目录 .dbsync-failed）
dbsync full -c config.yaml --recreate                     # 重跑：先 DROP 目标同名表/序列（数据不可恢复）再重建重灌

# 校验（迁移后跑；发现差异时退出码 3）
dbsync verify -c config.yaml
dbsync verify -c config.yaml --mode sampled --buckets 32 --sample-buckets 8 --report report.json

# 增量补数：逐表按水位/回退策略同步新增与修改（前置：已用 full 建好目标结构）
dbsync sync -c config.yaml
dbsync sync -c config.yaml --state /var/lib/dbsync/appdb.state

# 主键对账：源库已物理删除、目标仍残留的行（默认只报告；差异同样退出码 3）
dbsync reconcile -c config.yaml
dbsync reconcile -c config.yaml --max-keys 200000 --delete-orphans

# 口令加密：输出 ${enc:v1:...} 片段粘进配置（主密钥见 README「主密钥」一节）
export DBSYNC_MASTER_KEY='内网主密钥至少 8 位'
echo -n '真实口令' | dbsync encrypt-password
```

退出码：`0` 成功、`1` 运行期失败（配置/连接/迁移）、`2` 用法或参数错误、
`3` 发现差异（`verify` 校验不一致、`reconcile` 有孤儿/缺失或被跳过的表）。连接串与错误消息中的口令一律脱敏。

失败清单：`full` 跑挂时会写 `.dbsync-failed`（默认配置文件同目录，`--failed-list <file>` 可改），
里面写明失败阶段/表/主键区间、已完成/失败/未开始的表与重跑步骤——重跑前先看它，不用翻日志回放。
**重跑要加 `--recreate`**：建表/建序列/建索引不幂等，目标已有同名对象时会停在结构阶段，
`--recreate` 会先 DROP 目标同名表/序列（**数据不保留**）再重建重灌；只想补数据用 `sync`。

## 离线发布物

```bash
mvn -o -pl dbsync-dist -am package     # → dbsync-dist/target/dist/
cd dbsync-dist/target/dist && bash pack.sh && ls ..   # → dbsync-0.1.0-SNAPSHOT.tar.gz
```

解包后：把 `kingbase8.jar` 放进 `lib/`，复制 `config/dbsync.yaml.example` 改连接串，
然后 `bash bin/dbsync plan -c config.yaml`。主密钥两种来源：环境变量 `DBSYNC_MASTER_KEY`（或指向文件的
`DBSYNC_MASTER_KEY_FILE`）；`encrypt-password` 另外支持 `--master-key-file`。主密钥丢失则密文不可恢复。
要求 JRE 17+（不依赖 JDK/Maven/联网）。

**现场部署交给运维**：发布包内自带 `docs/deployment-guide.md`（部署与运维手册）——环境要求、10 分钟部署步骤、
配置与主密钥、切换 Runbook、常见报错对照、定时任务、升级回滚、上线检查清单都在里面；
仓库内同一份文件在 `dbsync-dist/src/main/dist/docs/deployment-guide.md`。

切换前的门禁：`bash bin/dbsync-cutover -c config.yaml`（`sync → verify`，两步都过才提示「可以切换」；
退出码 `3` = 校验发现差异，别带着差异切）。

## 桌面版（GUI）

现场同学记不住参数时用图形界面：**同一个 YAML、同一套编排**，界面动作与子命令一一对应
（日志里会打印「等价命令」便于转命令行复现）。

```bash
java -jar dbsync-gui/target/dbsync-gui-0.1.0-SNAPSHOT-shaded.jar   # 或发布物里的 bin/dbsync-gui
java -Djava.awt.headless=true -jar ...-shaded.jar                  # 无界面环境：给提示并退出 2
```

- **配置页**：选 YAML → 显示脱敏摘要；口令可临时覆盖（不落盘、不写日志、不持久化）；
  主密钥走 `--master-key-file` 等价控件或 `DBSYNC_MASTER_KEY`/`DBSYNC_MASTER_KEY_FILE`；
  内置「明文 → `${enc:v1:...}`」小工具；「另存 DDL」保存上次结构预览的 SQL（写盘前再脱敏）。
- **操作页**：五个动作 + 并行/分片/批量加载/单批上限/「重建（recreate）」/校验模式与桶数/报告文件/
  对账上限/删孤儿/状态文件；破坏性动作（全量迁移、删除孤儿行）先弹确认框，勾了「重建」再红字提示；
  进度条为不确定态（core 无进度回调）+ 计时 + 「中断」。
- **日志页**：实时追加（容量上限内滚动）、清空、复制、保存（保存前再脱敏一遍）。
- 退出码语义与 CLI 一致：`0` 成功、`1` 失败、`3` 发现差异（界面上是橙色提示而非错误弹窗）；
  中断是**尽力而为**（依赖 JDBC 在语句边界响应），已提交批次保留；重跑 `full` 需勾选
  「重建（recreate）」（等价 `--recreate`），`sync` 本身幂等。
- 与命令行共用同一份 DDL 渲染与失败清单：`另存 DDL` 的内容等于 `dbsync plan --out`，
  `full` 失败时界面日志里会给出 `.dbsync-failed` 的落盘路径。
- 无图形会话（跳板机/无 X11）会直接给一句中文提示并退出 2；麒麟/UOS 上中文显示成方框时装中文字体
  （`fonts-wqy-zenhei`/`fonts-noto-cjk`）。

## 已知限制

- **默认值翻译范围有限**：支持字面量（数值/字符串，含 `N'…'`，`bit` 列 `0/1`→`false`/`true`，字符列数值加引号）、
  `getdate()`/`sysdatetime()`/`sysdatetimeoffset()`→`now()`、`getutcdate()`/`sysutcdatetime()`→`now() at time zone 'utc'`、
  `newid()`/`newsequentialid()`→`gen_random_uuid()`（需目标库提供该函数，产 `DEFAULT_FUNC_PORTABILITY` 告警）、
  两参 `CONVERT` 单层展开；自增列走 `set default nextval(...)`。
  默认值引用源库对象（`NEXT VALUE FOR`、自定义函数）或含算式等无法识别的表达式仍丢弃并产 `DEFAULT_DROPPED` 告警，需人工补。
- **只读 `dbo`**：其它 schema 的表不迁移，但不再静默——源库存在非 `dbo` 表时 `plan`/`full` 会产
  `TABLES_OUTSIDE_SCOPE` 告警（只报数量与 schema 名，不读内容）；外键越界另有 `FK_REF_OUTSIDE_SCOPE`。
- **计算列、过滤索引、索引 INCLUDE 列**跳过或降级，均产告警。
- **重跑 `full` 必须加 `--recreate`**：建序列/建表/建索引都不是幂等的，目标库已有同名对象时
  会停在结构阶段（`relation "xxx_id_seq" already exists`）。`--recreate` 先
  `DROP TABLE ... CASCADE`（顺带删掉引用它的外键）再重建重灌，**目标同名表的数据不保留**；
  目标库若是多人共用，执行前务必确认。无断点续传：中途失败按 `--recreate` 整体重跑，
  或结构完好时用 `sync` 只补数据。
- **增量补数（`sync`）的边界**：抓不到源库的物理 `DELETE`（水位只看新增/修改），靠 `reconcile` 兜底；
  `pk-append` 只补缺失主键、不发现更新；无主键表只能用 `full-reload`。
  默认 5 秒回溯窗口会**故意重捞窗口内的行**（upsert 幂等、不留重复，但 `rowsSynced` 含重叠），
  追求「无变化即 0 行」时把 `watermarkLookbackSeconds` 设为 `0`。
  状态文件是单机本地状态：换机器/删文件只会退化为「重新全量拉取一次」（幂等，无数据损坏风险）；
  跨机器时钟需 NTP 对齐。达梦的 `merge ... using (select ? from dual)` upsert **未在真实 DM8 上执行过**，
  有环境后必须逐条确认。
- **并行/分片**：`parallelThreads × shards` 会同时占用目标库连接与资源，默认串行；分片只对「单列整数主键」
  生效（其它主键自动回退单分片并产 `SHARD_UNSUPPORTED_PK` 告警，正确性不受影响）；
  并行下失败同样是 fail-fast（已提交批次不回退，重跑加 `--recreate` 整轮重来）。
- **金仓 `COPY` 未在真实金仓验证**：`bulkLoad: copy` 经反射调用 PG 系驱动的
  `CopyManager#copyIn(String, Reader)`，本环境用 PG 官方驱动跑通同一路径；金仓驱动的类名/签名若不同，
  需按驱动文档改 `copyManagerClass`/`copyBaseConnectionClass`（默认由包名前缀推断）。
  **达梦 `dmfldr` 未实现**：配置即报错，达梦大表只能走 `bulkLoad: jdbc`。
- **口令加密的边界**：AES-256-GCM + PBKDF2（20 万次迭代，随机盐/IV），主密钥不落盘到配置文件；
  但主密钥仍由运维保管——丢失即不可恢复，且以环境变量注入时同机 root 可读 `/proc/<pid>/environ`。
  脱敏只覆盖「连接串/已知口令/常见参数名」，表里本就存在的敏感业务数据不在范围。
- 索引名落地为 `<表>_<索引>`（SQL Server 索引名表内唯一、金仓/PG 模式内唯一，必须限定）。
- **达梦方言未在真实实例验证**（本环境无 DM 实例与 `dm.jdbc` 驱动，仅纯单测覆盖）：`varchar2(n char)`、
  `timestamp with time zone`、匿名块序列重置、`OffsetDateTime` 绑定四处最需在有 DM 环境后逐条确认；
  达梦标识符要求实例按 `CASE_SENSITIVE=0` 建库（`plan` 会产 `DM_CASE_INSENSITIVE_REQUIRED` 提示）；
  `newid()` 无确认等价函数，一律丢弃并产 `DEFAULT_DROPPED` 人工指定（如 `SYS_GUID()`）。
  达梦驱动的 `dm.jdbc.driver.DmDriver` 不内置，需 `-cp` 提供。
- **校验（`verify`）的边界**：校验和是非加密哈希（理论上可碰撞，不做逐行 diff）；只校验源库 dbo 下的表，
  目标库多出来的表不在范围；抽样只覆盖选中桶，需要确定性结论时用默认的 `--mode full`；
  **迁移后必须跑一次，容器用例需 Docker 环境复验**。

## 目录

- `dbsync-core/`：`model` / `source` / `dialect` / `schema` / `transfer` / `job` / `verify` / `state` / `reconcile`
- `dbsync-cli/`：picocli 命令行壳与 YAML 配置
- `dbsync-gui/`：Swing 桌面壳（`gui/model` 承载可测逻辑，`gui/swing` 只做控件装配）
- `dbsync-dist/`：离线发布物（`src/main/dist` 为骨架，构建产出 `target/dist`）
  - 面向现场的手册：`dbsync-dist/src/main/dist/docs/deployment-guide.md`（随包分发）

## 许可证

[MIT](LICENSE)。第三方依赖各自遵循其许可证（picocli / snakeyaml：Apache-2.0，mssql-jdbc：MIT，
PostgreSQL JDBC：BSD-2-Clause）；**人大金仓与达梦的 JDBC 驱动不随本仓库/发布包分发**，
需自行从官方渠道获取并放入 `lib/`。
