# Dameng (DM) Database Driver for Go / 达梦数据库 Go 驱动

[![GoDoc](https://pkg.go.dev/badge/github.com/yxx1912008/dm-driver.svg)](https://pkg.go.dev/github.com/yxx1912008/dm-driver)

## Overview / 概述

Dameng (DM) Database Driver for Go is a pure Go implementation of the database/sql driver for connecting to Dameng databases. This driver enables Go applications to connect to Dameng database servers, execute queries, and manage transactions.

达梦数据库 Go 驱动是一个纯 Go 实现的 database/sql 驱动程序，用于连接达梦数据库。此驱动程序使 Go 应用程序能够连接到达梦数据库服务器、执行查询和管理事务。

## Features / 特性

- Full compatibility with Go's `database/sql` package / 完全兼容 Go 的 `database/sql` 包
- Support for connection pooling / 支持连接池
- Transaction support / 支持事务
- Prepared statements / 支持预编译语句
- SSL/TLS encryption support / 支持 SSL/TLS 加密
- Compression support / 支持压缩
- IPv6 support / 支持 IPv6
- LOB (Large Object) support for BLOB and CLOB / 支持 BLOB 和 CLOB 大对象
- Support for stored procedures and functions / 支持存储过程和函数
- Connection failover and load balancing / 支持连接故障转移和负载均衡
- Support for dynamic service names / 支持动态服务名

## Installation / 安装

To install the Dameng database driver, use `go get`:

要安装达梦数据库驱动，请使用 `go get`：

```bash
go get github.com/yxx1912008/dm-driver
```

## Usage / 使用方法

### Basic Connection / 基本连接

```go
package main

import (
    "database/sql"
    "fmt"
    "log"
    
    _ "github.com/yxx1912008/dm-driver"
)

func main() {
    // Connect to the database / 连接到数据库
    db, err := sql.Open("dm", "dm://username:password@hostname:port")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Test the connection / 测试连接
    err = db.Ping()
    if err != nil {
        log.Fatal(err)
    }

    // Execute a query / 执行查询
    rows, err := db.Query("SELECT id, name FROM users WHERE id > ?", 0)
    if err != nil {
        log.Fatal(err)
    }
    defer rows.Close()

    // Process results / 处理结果
    for rows.Next() {
        var id int
        var name string
        err := rows.Scan(&id, &name)
        if err != nil {
            log.Fatal(err)
        }
        fmt.Printf("ID: %d, Name: %s\n", id, name)
    }

    // Check for errors after iteration / 在迭代后检查错误
    err = rows.Err()
    if err != nil {
        log.Fatal(err)
    }
}
```

### Connection String / 连接字符串

The connection string follows the format: / 连接字符串格式如下：

```
dm://user:password@host:port/database?param1=value1&param2=value2
```

Common parameters include: / 常用参数包括：

- `charset`: Character set encoding / 字符集编码
- `ssl`: Enable SSL connection (0/1) / 启用 SSL 连接 (0/1)
- `compress`: Enable compression (0/1) / 启用压缩 (0/1)
- `socketTimeout`: Socket timeout in seconds / Socket 超时（秒）
- `loginMode`: Login mode / 登录模式
- `doSwitch`: Enable connection switching (0/1/2) / 启用连接切换 (0/1/2)
- `driverReconnect`: Use driver's reconnect mechanism / 使用驱动自身重连机制

Example with parameters: / 带参数的示例：

```
dm://myuser:mypass@localhost:5236?charset=utf8&ssl=1&compress=1
```

### Dynamic Service Name / 动态服务名

Support for dynamic service names in connection string: / 支持在连接字符串中使用动态服务名：

```
dm://user:password@GroupName?GroupName=(host1:port1,host2:port2,...)
```

Example: / 示例：

```
dm://myuser:mypass@CLUSTER_GROUP?CLUSTER_GROUP=(server1:5236,server2:5236,server3:5236)
```

### Transactions / 事务

```go
// Begin a transaction / 开始事务
tx, err := db.Begin()
if err != nil {
    log.Fatal(err)
}

// Execute statements / 执行语句
_, err = tx.Exec("INSERT INTO users(name, email) VALUES(?, ?)", "John Doe", "john@example.com")
if err != nil {
    tx.Rollback() // Rollback on error / 错误时回滚
    log.Fatal(err)
}

err = tx.Commit() // Commit the transaction / 提交事务
if err != nil {
    log.Fatal(err)
}
```

### Prepared Statements / 预编译语句

```go
stmt, err := db.Prepare("SELECT id, name FROM users WHERE age > ?")
if err != nil {
    log.Fatal(err)
}
defer stmt.Close()

rows, err := stmt.Query(18)
if err != nil {
    log.Fatal(err)
}
defer rows.Close()

for rows.Next() {
    var id int
    var name string
    err := rows.Scan(&id, &name)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("ID: %d, Name: %s\n", id, name)
}
```

## Configuration Options / 配置选项

The driver supports various configuration options through connection string parameters: / 驱动程序通过连接字符串参数支持各种配置选项：

| Parameter / 参数 | Description / 描述 | Default / 默认值 |
|------------------|---------------------|------------------|
| `user` | Database username / 数据库用户名 | - |
| `password` | Database password / 数据库密码 | - |
| `host` | Database host / 数据库主机 | localhost |
| `port` | Database port / 数据库端口 | 5236 |
| `charset` | Character set / 字符集 | GB18030 |
| `ssl` | SSL connection (0=off, 1=on) / SSL 连接 (0=关闭, 1=开启) | 0 |
| `compress` | Compression (0=off, 1=on) / 压缩 (0=关闭, 1=开启) | 0 |
| `socketTimeout` | Socket timeout in seconds / Socket 超时（秒） | 30 |
| `loginMode` | Login mode / 登录模式 | 4 |
| `doSwitch` | Connection switching (0=off, 1=on, 2=auto) / 连接切换 (0=关闭, 1=开启, 2=自动) | 1 |
| `driverReconnect` | Use driver's reconnect mechanism / 使用驱动自身重连机制 | true |

## API Reference / API 参考

The driver implements the standard `database/sql/driver` interface. Key types include: / 驱动程序实现标准的 `database/sql/driver` 接口。主要类型包括：

- `DmDriver`: The main driver implementation / 主驱动程序实现
- `DmConnection`: Represents a connection to the database / 表示到数据库的连接
- `DmStatement`: Represents a prepared statement / 表示预编译语句
- `DmResult`: Represents the result of an execution / 表示执行结果
- `DmRows`: Represents query results / 表示查询结果

## Error Handling / 错误处理

The driver provides detailed error information: / 驱动程序提供详细的错误信息：

```go
rows, err := db.Query("SELECT * FROM nonexistent_table")
if err != nil {
    // Type assertion to get detailed error / 类型断言以获取详细错误
    if dmErr, ok := err.(*dm.DmError); ok {
        fmt.Printf("Error Code: %d\n", dmErr.Code)
        fmt.Printf("Error Message: %s\n", dmErr.Message)
        // Get stack trace if needed / 如需堆栈跟踪
        // fmt.Println(dmErr.Stack())
    } else {
        fmt.Printf("General error: %v\n", err)
    }
}
```

## Version Information / 版本信息

Current version: 8.1.4.170 / 当前版本：8.1.4.170  
Build date: 2025.11.14 / 构建日期：2025.11.14  
SVN revision: 43114 / SVN 修订版：43114

## Changelog / 更新日志

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes. / 详细更新说明请参见 [CHANGELOG.md](CHANGELOG.md)。

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

欢迎贡献！请随时提交拉取请求。对于重大更改，请先打开一个议题讨论您想要更改的内容。

1. Fork the project / Fork 项目
2. Create your feature branch (`git checkout -b feature/AmazingFeature`) / 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`) / 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`) / 推送到分支 (`git push origin feature/AmazingFeature`)
5. Open a Pull Request / 打开拉取请求

## License / 许可证

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details. / 此项目根据 Apache 2.0 许可证授权 - 详情请参阅 [LICENSE](LICENSE) 文件。

## Support / 支持

For support, please contact Dameng support team or open an issue in this repository. / 如需支持，请联系达梦支持团队或在此仓库中打开议题。

## GORM Integration / GORM 集成

The driver supports integration with GORM v1 and v2 ORM frameworks. See the dialect package in the Dameng installation directory for detailed usage instructions.

驱动程序支持与 GORM v1 和 v2 ORM 框架集成。有关详细使用说明，请参见达梦安装目录中的方言包。