# Hangfire.GaussDB

[![NuGet](https://img.shields.io/badge/nuget-TSR.Hangfire.GaussDB-blue)](https://www.nuget.org/packages/TSR.Hangfire.GaussDB/)
[![TargetFrameworks](https://img.shields.io/badge/Target-net8.0%20%7C%20net9.0%20%7C%20net10.0-512bd4)](https://dotnet.microsoft.com/)

**Hangfire 的 GaussDB（华为云数据库）存储实现。**

---

## 简介

`Hangfire.GaussDB` 是一个 .NET 库，使 [Hangfire](https://www.hangfire.io/) 后台任务框架能够使用 **GaussDB** 作为持久化存储后端。它由成熟的 [Hangfire.PostgreSql](https://github.com/frankhommers/Hangfire.PostgreSql)（v1.9.4）改造而来，将 `Npgsql` 驱动替换为 `HuaweiCloud.GaussDB.Driver`（v8.0.1），同时完整保留了原有的存储算法、SQL 脚本、配置默认值与异常行为。

> 适用于华为云 GaussDB 环境。

---

## 安装

通过 NuGet 安装：

```bash
dotnet add package TSR.Hangfire.GaussDB
```

支持的目标框架：`net8.0`、`net9.0`、`net10.0`。

---

## 快速开始

### 1. 注册存储

在 `Startup.cs` 或 `Program.cs` 中配置 Hangfire 使用 GaussDB：

```csharp
using Hangfire;

// 使用连接字符串
services.AddHangfire(config =>
    config.UseGaussDBStorage(c =>
        c.UseGaussDBConnection(Configuration.GetConnectionString("HangfireConnection"))));
```

### 2. 配置连接字符串

在 `appsettings.json` 中添加 GaussDB 连接字符串：

```json
{
  "ConnectionStrings": {
    "HangfireConnection": "Host=localhost;Port=8000;Database=hangfire;Username=dbuser;Password=secret"
  }
}
```

### 3. 启动 Hangfire

```csharp
app.UseHangfireServer();
app.UseHangfireDashboard();
```

完成！Hangfire 将自动在 GaussDB 中创建 `hangfire` schema 及所需的全部数据表。

---

## 配置选项

`GaussDBStorageOptions` 提供了丰富的可配置参数：

| 属性 | 类型 | 默认值 | 中文含义 |
|------|------|--------|----------|
| **QueuePollInterval** | `TimeSpan` | 15 秒 | **队列轮询间隔** — Worker 在队列无作业时，等待此时间后再次查询。最小值 50ms（需设 AllowUnsafeValues） |
| **InvisibilityTimeout** | `TimeSpan` | 30 分钟 | **不可见超时** — 作业被取出后在此时间内不会被其他 Worker 重复获取。滑动模式下可通过心跳持续延长 |
| **DistributedLockTimeout** | `TimeSpan` | 10 分钟 | **分布式锁超时** — 获取分布式锁的最大等待时间（如过期清理、调度器等功能使用的锁） |
| **TransactionSynchronisationTimeout** | `TimeSpan` | 500 毫秒 | **事务同步超时** — 写事务并发冲突（序列化失败/唯一键冲突）时进行重试的总时长 |
| **JobExpirationCheckInterval** | `TimeSpan` | 1 小时 | **作业过期检查间隔** — 后台清理进程 ExpirationManager 每次运行的间隔 |
| **CountersAggregateInterval** | `TimeSpan` | 5 分钟 | **计数器聚合间隔** — CountersAggregator 定期将 counter 明细表归并到 aggregatedcounter 汇总表的间隔 |
| **DeleteExpiredBatchSize** | `int` | 1000 | **过期删除批次大小** — 每次清理过期记录时单批次最多删除的行数 |
| **AllowUnsafeValues** | `bool` | false | **允许不安全值** — 设为 true 后才允许设置极低的轮询间隔等值；设为 true 会绕过安全下限校验 |
| **UseNativeDatabaseTransactions** | `bool` | true | **使用原生数据库事务** — true 时用 `FOR UPDATE SKIP LOCKED` 出队；false 时用乐观锁（UpdateCount） |
| **PrepareSchemaIfNecessary** | `bool` | true | **自动准备 Schema** — 启动时是否自动安装/升级数据库表结构 |
| **SchemaName** | `string` | `"hangfire"` | **Schema 名称** — 所有 Hangfire 表所在的 PostgreSQL schema |
| **EnableTransactionScopeEnlistment** | `bool` | true | **启用事务登记** — 数据库连接是否自动登记到环境 TransactionScope 中；关闭可避免 prepared transaction 风险 |
| **EnableLongPolling** | `bool` | false（默认值未显式设置，bool 默认为 false） | **启用长轮询** — 启用 PostgreSQL 的 NOTIFY/LISTEN 异步通知机制，减少无作业时的数据库轮询开销 |
| **UseSlidingInvisibilityTimeout** | `bool` | false | **使用滑动不可见超时** — 启用后后台心跳进程会持续更新 fetchedat 时间戳，防止长时间运行的作业超时被其他 Worker 抢走。**注意**：如果服务器配置了 `IsLightweightServer` 则无效 |
| **EnableResilientStartup** (只读) | `bool` | 由 Retries > 0 计算 | **启用弹性启动** — 当 `StartupConnectionMaxRetries > 0` 且 `PrepareSchemaIfNecessary = true` 时自动启用，启动时连接失败会重试而非立即失败 |
| **StartupConnectionMaxRetries** | `int` | 5 | **启动连接最大重试次数** — 弹性启动时额外连接尝试次数（不含首次）。设为 0 禁用重试 |
| **StartupConnectionBaseDelay** | `TimeSpan` | 1 秒 | **启动重试基础延迟** — 弹性启动时指数退避计算的基础等待时间 |
| **StartupConnectionMaxDelay** | `TimeSpan` | 1 分钟 | **启动重试最大延迟** — 两次启动重试之间的最大等待上限 |
| **AllowDegradedModeWithoutStorage** | `bool` | true | **允许无存储降级运行** — 启用弹性启动且所有重试都失败时，不抛异常而是以降级模式启动，等待首次使用时再尝试初始化 |


---

## 数据库 Schema

库会自动创建以下表（位于 `hangfire` schema 中）：

| 表名 | 用途 |
|------|------|
| `hangfire.job` | 任务主表（invocation data、arguments 为 JSONB） |
| `hangfire.state` | 任务状态历史 |
| `hangfire.jobparameter` | 任务参数表 |
| `hangfire.jobqueue` | 任务队列表 |
| `hangfire.server` | 服务器心跳注册表 |
| `hangfire.hash` | 键-字段-值 哈希存储 |
| `hangfire.list` | 键-值 列表存储 |
| `hangfire.set` | 键-值-分 集合存储 |
| `hangfire.counter` | 计数器存储 |
| `hangfire.aggregatedcounter` | 聚合计数器 |
| `hangfire.lock` | 分布式锁资源表 |
| `hangfire.schema` | Schema 版本管理 |

所有表使用 GaussDB 的 `ORIENTATION=ROW` 存储参数，支持自动迁移升级。

---

## 高级用法

### 使用已有连接

```csharp
GaussDBConnection existingConnection = /* 你的 GaussDB 连接 */;

services.AddHangfire(config =>
    config.UseGaussDBStorage(c =>
        c.UseExistingGaussDBConnection(existingConnection)));
```

### 使用连接工厂

```csharp
services.AddHangfire(config =>
    config.UseGaussDBStorage(c =>
        c.UseConnectionFactory(myConnectionFactory)));
```

### 自定义 Schema 名称

```csharp
services.AddHangfire(config =>
    config.UseGaussDBStorage(c =>
        c.UseGaussDBConnection(connectionString),
        new GaussDBStorageOptions { SchemaName = "myhangfire" }));
```

---

## 与 Hangfire.PostgreSql 的关系

本库是 [Hangfire.PostgreSql](https://github.com/frankhommers/Hangfire.PostgreSql) v1.9.4 的直接改造成果：

- **保留**：所有存储逻辑、SQL 脚本、配置默认值、异常语义
- **替换**：`Npgsql` 驱动 → `HuaweiCloud.GaussDB.Driver` v8.0.1
- **适配**：连接工厂、异常分类、NOTIFY 通知机制改为使用华为 GaussDB 驱动 API
- **验证**：通过单元测试套件确保行为一致性

---

## 致谢

- [Frank Hommers](https://github.com/frankhommers) 及 Hangfire.PostgreSql 的所有贡献者
- [Sergey Odinokov](https://github.com/odinokov) — Hangfire 作者

---

## 相关链接

- [Hangfire 官网](https://www.hangfire.io/)
- [Hangfire GitHub](https://github.com/HangfireIO/Hangfire)
- [Hangfire.PostgreSql](https://github.com/frankhommers/Hangfire.PostgreSql)
- [华为云 GaussDB 文档](https://support.huaweicloud.com/gaussdb/)
- [本项目代码仓库](https://github.com/JASONPANZ/Hangfire.GaussDB)
