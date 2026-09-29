# TiDB Cloud 插件      (该项目有问题!!!!!!!!!)

这是一个为 astrbot 开发的插件，用于连接 TiDB Cloud 提供的免费 5GB 存储数据库。该插件基于 [astrbot_plugin_mysql](https://github.com/Chris95743/astrbot_plugin_mysql) 项目进行二次开发，在支持 MySQL 数据库连接的基础上，追加了对 TiDB Cloud 的支持，包括 SSL 证书验证功能。

## 项目来源

本项目基于 [Chris](https://github.com/Chris95743) 开发的 [astrbot_plugin_mysql](https://github.com/Chris95743/astrbot_plugin_mysql) 项目进行二次开发。原项目是一个功能强大的 MySQL 数据库管理插件，本项目在其基础上增加了对 TiDB Cloud 的专门支持。

## 功能特点

- 支持连接多个 TiDB Cloud 和 MySQL 数据库
- 提供完整的 WebUI 界面，用于管理数据库连接和执行 SQL 查询
- 支持 SSL 证书验证（TiDB Cloud 推荐）
- 连接池管理，提高性能
- 权限控制，防止危险操作
- 审计日志，记录所有数据库操作
- 支持通过 LLM 工具调用数据库功能

## 安装方法

1. 确保你的 Python 版本 >= 3.10

2. 克隆本项目：
```bash
git clone <项目地址>
cd astrbot_plugin_connect_tidb
```

3. 安装依赖：
```bash
pip install -e .
```

4. 将插件目录复制到 astrbot 的插件目录中

## 配置说明

插件启动后，会自动创建默认配置文件。你可以通过以下方式配置插件：

### 1. WebUI 配置

插件启动后，默认会在 6200 端口启动 WebUI 服务。你可以通过浏览器访问 `http://localhost:6200` 来配置插件。

默认用户名：`admin`
默认密码：`admin`

### 2. 配置文件

配置文件位于插件的数据目录下，文件名为 `config.json`。你也可以直接编辑该文件来配置插件。

#### 配置示例

```json
{
  "version": "1.0",
  "webui_username": "admin",
  "webui_password": "admin",
  "webui_port": 6200,
  "connections": {
    "tidb_cloud": {
      "host": "xxx.tidbcloud.com",
      "port": 4000,
      "user": "root",
      "password": "your_password",
      "database": "test",
      "enable_ssl": true,
      "ssl_ca": "/path/to/ca.pem",
      "pool_size": 5,
      "pool_recycle": 3600,
      "pool_timeout": 30
    },
    "local_mysql": {
      "host": "localhost",
      "port": 3306,
      "user": "root",
      "password": "your_password",
      "database": "test",
      "enable_ssl": false,
      "pool_size": 5,
      "pool_recycle": 3600,
      "pool_timeout": 30
    }
  },
  "permissions": {
    "max_query_result_rows": 1000,
    "max_update_rows": 1000,
    "max_delete_rows": 1000,
    "allow_danger_sql": false
  }
}
```

## 使用方法

### 1. 通过 WebUI 使用

1. 访问 `http://localhost:6200` 并登录
2. 在 "连接管理" 页面添加 TiDB Cloud 或 MySQL 数据库连接
3. 在 "SQL 查询" 页面执行 SQL 查询
4. 在 "审计日志" 页面查看所有数据库操作记录

### 2. 通过 astrbot 指令使用

#### 基本指令

- `/tidb help`: 查看插件帮助信息
- `/tidb status`: 查看插件状态
- `/tidb connections`: 查看所有数据库连接
- `/tidb test <连接名>`: 测试指定连接是否可用
- `/tidb query <连接名> <SQL>`: 执行SQL查询

#### 群聊中@机器人的操作示例

在群聊中，你可以通过@机器人并发送命令来使用插件功能。

##### 示例1：查看插件帮助
```
@机器人 /tidb help
```

机器人会返回：
```
TiDB Cloud 数据库管理指令帮助：
/tidb status - 查看插件状态
/tidb connections - 查看所有数据库连接
/tidb test <连接名> - 测试指定连接是否可用
/tidb query <连接名> <SQL> - 执行SQL查询
/tidb insert <连接名> <SQL> - 执行SQL插入
/tidb update <连接名> <SQL> - 执行SQL更新
/tidb delete <连接名> <SQL> - 执行SQL删除
/tidb webui - 查看WebUI地址
```

##### 示例2：查看插件状态
```
@机器人 /tidb status
```

机器人会返回：
```
TiDB Cloud 插件状态：
已加载连接数量: 2
连接池状态：
  - tidb_cloud: 活跃=0, 空闲=3, 总数=3
  - local_mysql: 活跃=0, 空闲=3, 总数=3
```

##### 示例3：执行SQL查询
```
@机器人 /tidb query tidb_cloud SELECT * FROM users LIMIT 5
```

机器人会返回：
```
查询成功（共 5 行）：
| id | name    | email                | created_at          |
|----|---------|----------------------|---------------------|
| 1  | Alice   | alice@example.com    | 2023-01-01 10:00:00 |
| 2  | Bob     | bob@example.com      | 2023-01-02 11:00:00 |
| 3  | Charlie | charlie@example.com  | 2023-01-03 12:00:00 |
| 4  | David   | david@example.com    | 2023-01-04 13:00:00 |
| 5  | Eve     | eve@example.com      | 2023-01-05 14:00:00 |
```

##### 示例4：测试数据库连接
```
@机器人 /tidb test tidb_cloud
```

机器人会返回：
```
✅ 连接 'tidb_cloud' 测试成功：连接到 TiDB Cloud 成功
```

#### 通过 LLM 工具使用

插件会自动向 LLM 注册以下工具：

1. `tidb_query`: 执行 SQL 查询
2. `tidb_insert`: 执行 SQL 插入
3. `tidb_update`: 执行 SQL 更新
4. `tidb_delete`: 执行 SQL 删除
5. `tidb_create_table`: 创建表
6. `tidb_show_schema`: 查看数据库结构

## TiDB Cloud 连接说明

### 获取 TiDB Cloud 连接信息

1. 登录 TiDB Cloud 控制台
2. 创建或选择一个集群
3. 在 "连接" 页面获取连接信息：
   - 主机地址
   - 端口（默认 4000）
   - 用户名
   - 密码

### 配置 SSL 证书

TiDB Cloud 推荐使用 SSL 连接。你需要：

1. 下载 CA 证书（root.crt）
2. 在添加连接时启用 SSL，并指定 CA 证书的路径

## 安全注意事项

1. 请妥善保管 WebUI 的用户名和密码
2. 不要在公共网络上暴露 WebUI 服务
3. 建议禁用危险 SQL 操作（如 DROP、TRUNCATE 等）
4. 定期查看审计日志，确保没有异常操作

## 更新日志

### v1.1.0
- 初始版本，支持 TiDB Cloud 和 MySQL 数据库连接
- 提供完整的 WebUI 界面
- 支持 SSL 证书验证
- 连接池管理和权限控制
- 审计日志功能

## 许可证

本项目基于原项目的 [AGPL-3.0](https://github.com/Chris95743/astrbot_plugin_mysql/blob/main/LICENSE) 许可证进行二次开发，继承并遵守原许可证的所有条款。

### AGPL-3.0 许可证摘要

1. 你可以自由使用、修改和分发本软件
2. 如果你修改了本软件的源代码，你必须公开修改后的源代码
3. 如果你将本软件作为网络服务提供，你必须提供源代码给用户
4. 你必须保留原作者的版权声明和许可证文本
5. 本软件不提供任何担保，使用风险自行承担

## 联系方式

### 原项目作者
- **作者**: Chris
- **GitHub**: [@Chris95743](https://github.com/Chris95743)
- **原项目仓库**: [astrbot_plugin_mysql](https://github.com/Chris95743/astrbot_plugin_mysql)

### 本项目贡献者
- 如有问题或建议，请通过以下方式联系：
  - 项目地址：<项目地址>

  <!-- - 邮箱：<邮箱地址> -->
