# SSE（可搜索加密）框架集成改造说明

## 一、背景

我们在 openGauss 数据库中集成了 SSE（Searchable Symmetric Encryption）框架，使数据库具备在加密数据上执行 SQL 查询的能力。本次改造涉及客户端和服务端两侧，覆盖了 SQL 拦截、令牌生成、加密索引维护、服务端搜索执行等完整链路。

集成的 SSE 方案包括：

- **Fides / Sophos**：前向安全方案
- **Mitra**：支持多关键词查询，含 JOIN 支持
- **FBDSSE**：前向后向安全方案
- **Diana**：支持删除的前向安全方案
- **Dual**：支持动态更新的方案
- **CloseFB**：前向后向安全方案，含索引重建
- **Janus++**：支持删除与更新的方案

---

## 二、客户端通用模块（common.cpp）

### 2.1 SSE 框架引入与全局状态

引入了各 SSE 方案的客户端头文件及辅助模块（SSE_map、SSE_time、GMP 大数库），并新增全局 SSE 状态标志 `common_sseflag` 和 `common_delsseflag`，用于在查询执行过程中标记当前操作的 SSE 模式。

### 2.2 SQL 拦截与自动路由

在 SQL 执行入口处增加拦截逻辑：根据表名从 `sse_table_map` 查找该表对应的 SSE 加密模式，自动将原始 SQL 改写为带模式前缀的格式（如 `fides_select`、`fbdsse_insert` 等）。INSERT、DELETE、SELECT 操作分别路由到对应 SSE 方案的处理函数。

### 2.3 结果输出控制

SSE 模式下屏蔽了 `PrintQueryStatus` 等输出，避免加密中间信息泄露。

---

## 三、客户端查询执行模块（fe-exec.cpp）

### 3.1 SSE 客户端库集成

引入各 SSE 方案的客户端库及辅助模块（init_crypto、LocalTable），新增全局加密客户端实例 `Client_*`。

### 3.2 数据行处理中的加解密

在 `pqRowProcessor` 中增加了客户端加密列的检测与自动解密逻辑，确保应用层拿到的是明文结果。

### 3.3 SQL 改写与令牌生成

- **INSERT**：根据 SSE 模式调用对应客户端（Sophos_client、FBdsse_Client 等）生成加密索引和令牌，将原始 INSERT 改写为向 `_index` 表插入密文条目的 SQL
- **SELECT**：生成搜索令牌，改写为调用服务端存储函数的 SQL
- **DELETE**：为支持删除的方案（FBDSSE 等）生成删除令牌并改写 SQL
- **JOIN**：为 Mitra 方案增加了 JOIN 查询的专用改写逻辑

---

## 四、服务端查询处理模块（postgres.cpp）

### 4.1 SSE 服务端库集成

引入各 SSE 方案的服务端头文件（Server_Sophos、Server_FBDSSE、dual_server、closefb_server、januspp_server），以及 SSE 公共模块。

### 4.2 服务端 SQL 拦截与分发

在 `exec_simple_query` 中增加对 SSE 前缀 SQL 的识别和分发处理：

- **Sophos/Fides**：初始化服务端密钥，接收客户端搜索令牌后执行服务端搜索，返回加密索引条目
- **Diana**：初始化服务端，反序列化约束密钥，执行搜索并返回更新令牌列表
- **FBDSSE**：服务端搜索计算
- **Dual**：服务端删除和搜索令牌处理，通过 `dual_suedb` 执行加密索引更新
- 各方案均包含性能计时埋点（tracker），便于后续性能分析

---

## 五、整体架构

```
用户 SQL
  │
  ▼
客户端拦截（common.cpp / fe-exec.cpp）
  │  识别表名 → 查找 SSE 模式 → 改写 SQL + 生成令牌
  │
  ▼
服务端执行（postgres.cpp）
  │  识别 SSE 前缀 → 分发到对应方案 → 执行加密索引操作 → 返回密文结果
  │
  ▼
客户端后处理（fe-exec.cpp）
  │  解密结果行 → 返回明文给应用
```

改造的核心思路是：在数据库通信层透明地插入 SSE 加解密逻辑，上层应用无需感知底层数据已加密，仍以常规 SQL 方式交互。