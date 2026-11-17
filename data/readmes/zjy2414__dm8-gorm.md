# GORM DM8 Driver

达梦数据库（DM8）的 [GORM](https://gorm.io/zh_CN/) v2 方言驱动，开箱即用。

方言实现与达梦官方 `gorm_v2_dialect` 保持一致，驱动部分为达梦官方 Go 驱动（`8.1.5.88 / 2026.09.23`）源码，
无需再手动复制驱动到项目中。

## 特性

- 完整的 `gorm.Dialector` 实现：建连、类型映射、引用符、保存点
- **Upsert 支持**：`clause.OnConflict` 会被翻译为达梦 `MERGE INTO`，也可切换为 MySQL / PostgreSQL 兼容语法
- **自增列处理**：显式插入自增主键时自动 `SET IDENTITY_INSERT ... ON/OFF`，插入后回填自增 ID
- **迁移器**：基于达梦系统表判断表 / 列 / 索引 / 约束，支持 `AutoMigrate`、列注释（`COMMENT ON COLUMN`）
- 内置 `BuildUrl`，一行生成标准 DSN

## 环境要求

| 依赖 | 版本 |
| --- | --- |
| Go | 1.20+ |
| GORM | v2（`gorm.io/gorm` v1.31.2 已验证） |
| 达梦数据库 | DM8（驱动 `8.1.5.88`） |

## 安装

```shell
go get github.com/zjy2414/dm8-gorm
```

## 快速上手

包名为 `dameng`，与模块路径不同，建议显式起别名：

```go
package main

import (
	"log"

	dameng "github.com/zjy2414/dm8-gorm"
	"gorm.io/gorm"
)

type User struct {
	ID       uint64 `gorm:"primaryKey;autoIncrement"`
	Name     string `gorm:"size:50;comment:用户姓名"`
	Password string `gorm:"size:128;comment:登录密码"`
}

func main() {
	dsn := dameng.BuildUrl("SYSDBA", "SYSDBA", "127.0.0.1", 5236, map[string]string{
		"schema":         "SYSDBA",
		"appName":        "gorm-dm8-demo",
		"connectTimeout": "30000",
	})

	db, err := gorm.Open(dameng.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatalf("连接达梦数据库失败：%v", err)
	}

	if err = db.AutoMigrate(&User{}); err != nil {
		log.Fatalf("迁移表结构失败：%v", err)
	}

	db.Create(&User{Name: "someone", Password: "123456"})
}
```

## 连接配置

### BuildUrl

```go
dsn := dameng.BuildUrl(user, password, host, port, options...)
// dm://user:password@host:port?schema=SYSDBA&appName=xxx
```

`options` 为可变参数，可传入多个 `map[string]string`，最终合并为连接串属性。
属性说明见[官方文档](https://eco.dameng.com/document/dm/zh-cn/pm/go-rogramming-guide.html#11.3%20%E8%BF%9E%E6%8E%A5%E4%B8%B2%E5%B1%9E%E6%80%A7%E8%AF%B4%E6%98%8E)。

### Open / New

```go
// 仅指定 DSN
db, err := gorm.Open(dameng.Open(dsn), &gorm.Config{})

// 需要更多参数时使用 New
db, err := gorm.Open(dameng.New(dameng.Config{
	DriverName: dameng.DriverName,
	DSN:        dsn,
	GormMode:   0,
}), &gorm.Config{})
```

### Config

| 字段 | 说明 |
| --- | --- |
| `DriverName` | 驱动名，默认为 `dameng.DriverName`（`"dm"`） |
| `DSN` | 连接字符串 |
| `Conn` | 复用的 `gorm.ConnPool`，设置后不再新建连接 |
| `DefaultStringSize` | 未指定长度的 `string` 字段默认长度 |
| `GormMode` | Upsert 兼容模式：`0` 达梦原生（默认）、`1` MySQL 兼容、`2` PostgreSQL 兼容 |

## 数据类型映射

| GORM 类型 | 达梦类型 | 说明 |
| --- | --- | --- |
| `bool` | `BIT` | |
| `int` / `uint` | `TINYINT` / `SMALLINT` / `INT` / `BIGINT` | 按 `size`（8 / 16 / 32 / 64）选择，自增追加 `IDENTITY(1,1)` |
| `float` | `DECIMAL(p,s)` / `DOUBLE` | 指定 `precision` 时为 `DECIMAL` |
| `string` | `VARCHAR(n)` / `CLOB` | 长度按**字节**计；未指定长度且为主键 / 索引 / 有默认值时取 `255`；`size <= 0` 或 `>= 32768` 为 `CLOB` |
| `time.Time` | `TIMESTAMP` / `TIMESTAMP(p)` | 指定 `precision` 时带小数秒 |
| `[]byte` | `VARBINARY(n)` / `BLOB` | `size` 在 `1 ~ 32767` 之间为 `VARBINARY` |
| 其他 | 原样输出 | 自增追加 `IDENTITY(1,1)` |

标识符统一使用双引号 `"` 包裹，兼容大小写敏感（`CASE_SENSITIVE`）的库实例。

## Upsert

```go
// 主键冲突时更新全部字段
db.Clauses(clause.OnConflict{UpdateAll: true}).Create(&users)

// 冲突列由主键推断；也可显式指定并只更新部分字段
db.Clauses(clause.OnConflict{
	Columns:   []clause.Column{{Name: "id"}},
	DoUpdates: clause.AssignmentColumns([]string{"name", "password"}),
}).Create(&users)
```

三种 `GormMode` 的差异：

| GormMode | 生成语句 | 说明 |
| --- | --- | --- |
| `0`（默认） | `MERGE INTO ... USING (SELECT ... FROM DUAL) ON ... WHEN MATCHED / NOT MATCHED` | 达梦原生语法，冲突列缺省取模型主键 |
| `1` | `ON DUPLICATE KEY UPDATE` 兼容 | 以匿名块 + `DUP_VAL_ON_INDEX` 异常实现，兼容 MySQL 写法，支持 `UpdateAll` |
| `2` | `ON CONFLICT` 兼容 | 支持 `Columns`、`OnConstraint`、`Where`、`TargetWhere` |

`GormMode` 为 `1` 或 `2` 时，若结构体主键已有值，驱动会自动包一层 `SET IDENTITY_INSERT <表> ON/OFF`。

## 迁移

```go
db.AutoMigrate(&User{}, &Order{})
```

- 表 / 列 / 索引 / 约束的存在性均通过达梦系统表（`SYSOBJECTS`、`SYSCOLUMNS`、`SYSCONS` 等）判断
- 列注释在**建表、加列、改列**时通过 `COMMENT ON COLUMN` 写入（达梦不支持内联 `COMMENT`）
- 删除表使用 `DROP TABLE IF EXISTS ... CASCADE`

## 已知限制

- `UPDATE` / `DELETE` 子句不包含 `ORDER BY`（`LIMIT` 支持）
- 达梦不支持 `INSERT INTO ... DEFAULT VALUES`，空插入会使用 `NULL` 占位
- `GormMode` 读取自 `*Dialector`，请勿自定义包装 `Dialector` 后传入 `gorm.Open`

## 目录结构

```
.
├── dm.go        # Dialector：配置、类型映射、引用符、BuildUrl
├── create.go    # Create 回调：MERGE INTO / MySQL / PG 兼容 Upsert
├── migrator.go  # 迁移器
├── dm8/         # 达梦官方 Go 驱动（8.1.5.88）
└── dm_test.go   # 单元测试
```

## 参考文档

- 达梦产品手册：<https://eco.dameng.com/document/dm/zh-cn/pm/>
- DM Go 编程指南：<https://eco.dameng.com/document/dm/zh-cn/pm/go-rogramming-guide.html>
- 达梦常见问题：<https://eco.dameng.com/document/dm/zh-cn/faq/>
- GORM 官方文档：<https://gorm.io/zh_CN/docs/>

`dm8/` 目录内容来自达梦官方发布的 Go 驱动，版权归达梦数据库股份有限公司所有。
