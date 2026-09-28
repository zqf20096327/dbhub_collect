# MAS.Database

<p align="center">
  <img src="logo-RemoveBG.png" alt="Logo">
</p>

<p align="center">
  一个轻量但可演进的 ORM-like 基础设施层
</p>

<p align="center">
  <img src="https://img.shields.io/badge/.NET-8.0-blue" />
    <img src="https://img.shields.io/badge/license-Apache%202.0-green" />
  <a href="https://www.nuget.org/packages/MAS.Database/">
    <img src="https://img.shields.io/nuget/v/MAS.Database.svg" />
  </a>
  <img src="https://img.shields.io/badge/C%23-239120.svg?logo=csharp&logoColor=white" />
  <img src="https://img.shields.io/badge/IDE-Visual%20Studio-5C2D91?logo=visual-studio" />
</p>

## ✨ MAS 开放源代码

> 该库是 MAS 开放源代码体系中的一部分，专注于工业自动化场景下的数据库基础设施建设

如果你正在构建 WPF、WinUI、Worker Service 或 ASP.NET Core 应用，
并希望以统一、可扩展的方式管理数据库访问、实体映射与 SQL 生成，
那么 `MAS.Database` 可以作为你的基础设施层解决方案

该库提供：

- 统一的数据库操作抽象
- 可扩展的 SQL 生成机制
- 基于特性的实体建模方式
- 通用泛型仓储支持
- 多数据库类型扩展能力

适用于对 **可维护性、扩展性、工程化** 有较高要求的工业软件项目

## 🗺️ 发展路线

- [x] MySql（[MySqlConnector](https://github.com/mysql-net/MySqlConnector)）
- [ ] SqlServer
- [ ] PostgreSql
- [ ] Oracle
- [ ] SQLite

## ⚠️ 使用前提

在使用本项目之前，请确认你的应用满足以下条件：

- 使用 **现代 .NET 项目**
- 目标框架为 **.NET 8.0 及以上**
- 使用 **Microsoft.Extensions.DependencyInjection** 进行服务注册与解析
- 不支持仍运行在 **.NET Framework** 上的项目（未进行测试）
- 仅适合在 WPF / WinUI / Worker / ASP.NET Core 中集成

## 📦 NuGet

.NET CLI：

```bash
dotnet add package MAS.Database
```

Package Manager：

```bash
Install-Package MAS.Database
```

## 🚀 快速开始

以 **MySql** 为例，演示从 **服务注册 → 依赖注入 → 获取实例 → 测试连接** 的流程

### 注册服务

在应用启动阶段注册数据库服务：

```csharp
using Microsoft.Extensions.DependencyInjection;
using MAS.Database;

IServiceCollection services = new ServiceCollection();
_ = services.AddDatabase();
_ = services.AddRepositories(); // 可选的通用泛型仓储
```

### 数据库配置

实现`IDbConfig`示例如下：

```csharp
using MAS.Database;

public class DbConfig : IDbConfig {
    public DatabaseType Type => DatabaseType.MySql;

    public string Server { get; set; } = "127.0.0.1";
    public int Port { get; set; } = 3306;
    public string DatabaseName { get; set; } = "test_db";
    public string User { get; set; } = "root";
    public string Password { get; set; } = "123456";

    public string GetConnectionString() {
        return Type switch {
            DatabaseType.MySql => $"server={Server};user={User};database={DatabaseName};port={Port};password={Password};SslMode=Preferred;CharSet=utf8mb4;",
            _ => throw new NotSupportedException($"Database type {Type} is not supported."),
        };
    }

    public string GetServerConnectionString() {
        return Type switch {
            DatabaseType.MySql => $"server={Server};user={User};port={Port};password={Password};SslMode=Preferred;CharSet=utf8mb4;",
            _ => throw new NotSupportedException($"Database type {Type} is not supported."),
        };
    }
}
```

### 数据库初始化

以`MySql`为例，示例如下：

```csharp
using MAS.Database;

public class MainViewModel {
    private readonly IDbInitializerFactory _dbInitializerFactory;

    public MainViewModel(IDbInitializerFactory dbInitializerFactory) {
        _dbInitializerFactory = dbInitializerFactory;
    }

    public async Task InitializeDatabaseAsync() {
        var config = new DbConfig();
        var initializer = _dbInitializerFactory.Create(config);
        await initializer.InitializeDatabaseAsync();
    }
}
```

### 数据库操作

你可以通过这两个接口来获取数据库操作实例：

- `IDbOperationsProvider`：数据库操作实例提供器，创建 + 状态
- `IDbOperationsFactory`：数据库操作实例工厂，仅提供创建

以`MySql`为例，示例如下：

```csharp
using MAS.Database;

public class MainViewModel {
    private readonly IDbOperationsProvider _dbOperationsProvider;

    public MainViewModel(IDbOperationsProvider dbOperationsProvider) {
        _dbOperationsProvider = dbOperationsProvider;
    }
}
```

**获取数据库操作实例：**

```csharp
var config = new DbConfig();
var db = _dbOperationsProvider.GetOrCreate<IMySqlOperations>(config);
```

**执行命令（INSERT / UPDATE / DELETE）：**

```csharp
await db.ExecuteCommandAsync(
    "UPDATE user SET name = @name WHERE id = @id",
    cmd => {
        var p1 = cmd.CreateParameter();
        p1.ParameterName = "@name";
        p1.Value = "MAS";
        cmd.Parameters.Add(p1);

        var p2 = cmd.CreateParameter();
        p2.ParameterName = "@id";
        p2.Value = 1;
        cmd.Parameters.Add(p2);
    });
```

**查询数据：**

```csharp
var list = await db.ExecuteQueryAsync(
    "SELECT id, name FROM user",
    reader => new {
        Id = reader.GetInt32(0),
        Name = reader.GetString(1)
    });
```

**查询单条数据：**

```csharp
var user = await db.ExecuteSingleRowAsync(
    "SELECT id, name FROM user WHERE id = @id",
    reader => new {
        Id = reader.GetInt32(0),
        Name = reader.GetString(1)
    },
    cmd => {
        var p = cmd.CreateParameter();
        p.ParameterName = "@id";
        p.Value = 1;
        cmd.Parameters.Add(p);
    });
```

**查询标量值：**

```csharp
var count = await db.ExecuteScalarAsync<long>("SELECT COUNT(*) FROM user");
```

**事务操作：**

```csharp
await db.ExecuteInTransactionAsync(async tx => {
    await db.ExecuteCommandAsync(
        "INSERT INTO user(name) VALUES(@name)",
        cmd => {
            var p = cmd.CreateParameter();
            p.ParameterName = "@name";
            p.Value = "测试";
            cmd.Parameters.Add(p);
        },
        tx);
});
```

### 数据库仓储

前置条件：需要注册`AddRepositories`或自定义实现仓储，仓储模板：

```csharp
internal sealed class Repository<TEntity>(
    IDbOperations dbOperations,
    ISqlGeneratorFactory sqlGeneratorFactory)
    : RepositoryBase<TEntity>(dbOperations, sqlGeneratorFactory), IRepository<TEntity> where TEntity : class, new() {
}
```

**实体定义：**

```csharp
[CreationPriority(PriorityLevel.LevelA)]
[Table("Product_Info", DisplayName = "产品信息")]
[Index("IX_Product_Info_ProductId", "ProductId", IsUnique = true, Comment = "产品Id 唯一索引")]
[Index("IX_Product_Info_Code", "Code", Comment = "产品代码")]
public class ProductInfoEntity {
    [DisplayName("主键")]
    [Column("Id", "INT",
        IsPrimaryKey = true,
        IsAutoIncrement = true,
        IsNullable = false,
        Comment = "主键标识符，自增")]
    public int Id { get; set; }

    [DisplayName("产品Id")]
    [Column("ProductId",
        "VARCHAR(25)",
        IsNullable = false,
        IsUnique = true,
        Comment = "产品Id（业务唯一标识）")]
    public string ProductId { get; set; } = string.Empty;

    [DisplayName("产品名称")]
    [Column("ProductName",
        "VARCHAR(20)",
        IsNullable = false,
        Comment = "产品名称")]
    public string ProductName { get; set; } = string.Empty;

    [DisplayName("产品类型")]
    [Column("Type",
        "VARCHAR(20)",
        IsNullable = false,
        Comment = "产品类型")]
    public string Type { get; set; } = string.Empty;

    [DisplayName("产品代码")]
    [Column("Code",
        "VARCHAR(25)",
        IsNullable = false,
        Comment = "产品代码")]
    public string Code { get; set; } = string.Empty;

    [DisplayName("配方编号")]
    [Column("Recipe",
        "VARCHAR(25)",
        IsNullable = false,
        Comment = "配方编号")]
    public string Recipe { get; set; } = string.Empty;

    [DisplayName("备注信息")]
    [Column("Notes",
        "VARCHAR(50)",
        IsNullable = true,
        Comment = "备注信息")]
    public string? Notes { get; set; }

    [DisplayName("创建时间")]
    [Column("CreatedAt",
        "DATETIME",
        IsNullable = false,
        IsUpdatable = false,
        Comment = "创建时间")]
    public DateTime CreatedAt { get; set; }

    [DisplayName("更新时间")]
    [Column("UpdatedAt",
        "DATETIME",
        IsNullable = false,
        Comment = "更新时间")]
    public DateTime UpdatedAt { get; set; }
}
```

**注入仓储：**

```csharp
public sealed class ProductService {
    private readonly IRepository<ProductInfoEntity> _repository;

    public ProductService(IRepository<ProductInfoEntity> repository) {
        _repository = repository;
    }
}
```

**添加数据：**

```csharp
await _repository.AddAsync(new ProductInfoEntity {
    ProductId = "P001",
    ProductName = "测试产品",
    Type = "A",
    Code = "C001",
    Recipe = "R001",
    CreatedAt = DateTime.Now,
    UpdatedAt = DateTime.Now
});
```

**更新数据：**

```csharp
var entity = await _repository.GetByIdAsync(1);
if (entity is not null) {
    entity.ProductName = "测试产品-已更新";
    entity.Type = "B";
    entity.UpdatedAt = DateTime.Now;

    await _repository.UpdateAsync(entity);
}
```

**新增或更新：**

`AddOrUpdateAsync`会根据标注为`IsUnique = true`的字段判断是否已存在记录。
如果存在，则执行更新；如果不存在，则执行新增

```csharp
await _repository.AddOrUpdateAsync(new ProductInfoEntity {
    ProductId = "P001",
    ProductName = "测试产品",
    Type = "A",
    Code = "C001",
    Recipe = "R001",
    Notes = "自动新增或更新",
    CreatedAt = DateTime.Now,
    UpdatedAt = DateTime.Now
});
```

>注意：如果实体上定义了多个唯一字段，当前实现会优先使用第一个唯一字段作为判断依据

**删除数据：**

根据主键字段删除对应记录

```csharp
ProductInfoEntity? entity = await _repository.GetByIdAsync(1);
if (entity is not null) {
    await _repository.DeleteAsync(entity);
}
```

**根据字段查询：**

适合按业务字段获取单条记录，例如按产品编号查询

```csharp
ProductInfoEntity? entity = await _repository.GetByFieldAsync("ProductId", "P001");
```

**条件加载：**

```csharp
TableQueryParameters parameters = new() {
    PageIndex = 1,
    PageSize = 20
};

List<ProductInfoEntity> products = await _repository.LoadTableDataAsync(parameters);
```

**聚合查询：**

获取单个聚合值

```csharp
AggregateQueryParameters parameters = new() {
    AggregateExpression = "COUNT(*)"
};

long? count = await _repository.GetAggregateValueAsync<long>(parameters);
```

获取分组聚合列表

```csharp
AggregateQueryParameters parameters = new() {
    AggregateExpression = "COUNT(*) AS TotalCount",
    GroupByFields = ["Type"]
};

IEnumerable<Dictionary<string, object>> result = await _repository.GetAggregateListAsync(parameters);
```
