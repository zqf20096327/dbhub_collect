# ThinkPHP 6 达梦数据库(DM8)驱动

为 ThinkPHP 6 提供的达梦数据库（DM8）连接驱动和 SQL 构建器，基于 DM8 MySQL 兼容模式开发。

## 文件结构

```
extend/think/
├── db/
│   ├── connector/
│   │   └── Dm.php      # 数据库连接驱动
│   └── builder/
│       └── Dm.php      # SQL 构建器
└── README.md
```

## 环境要求

| 依赖 | 版本 |
|------|------|
| PHP | >= 7.2.5 |
| ThinkPHP | ^6.0.0 |
| think-orm | ^2.0 |
| 达梦数据库 | DM8 (MySQL 兼容模式) |
| PHP PDO 扩展 | PDO_DM |

## 部署方法

### 1. 安装 PDO_DM 扩展

确保 PHP 已安装达梦 PDO 驱动：

```bash
# 检查是否已安装
php -m | grep -i dm

# 若未安装，从达梦官方获取 PDO_DM 扩展并配置 php.ini
# extension=pdo_dm.so   (Linux)
# extension=php_pdo_dm.dll   (Windows)
```

### 2. 复制驱动文件

将 `think/db/` 目录放入 ThinkPHP 项目的 `extend/` 目录下：

```
your-project/
├── extend/
│   └── think/
│       └── db/
│           ├── connector/
│           │   └── Dm.php
│           └── builder/
│               └── Dm.php
```

### 3. 配置 Composer 自动加载

确保 `composer.json` 中配置了 extend 目录的自动加载（ThinkPHP 6 默认已配置）：

```json
{
    "autoload": {
        "psr-0": {
            "": "extend/"
        }
    }
}
```

更新自动加载：

```bash
composer dump-autoload
```

### 4. 配置数据库连接

编辑 `config/database.php`，添加达梦数据库连接配置：

```php
<?php

return [
    // 默认数据库连接
    'default' => env('database.driver', 'dm'),

    'connections' => [

        // ... 其他连接配置 ...

        'dm' => [
            // 数据库类型（must be 'dm'）
            'type'            => 'dm',
            // 服务器地址
            'hostname'        => env('database.hostname', '127.0.0.1'),
            // 数据库端口
            'hostport'        => env('database.hostport', '5236'),
            // 数据库名/模式名
            'database'        => env('database.database', 'EXAM_SYSTEM'),
            // 用户名
            'username'        => env('database.username', 'SYSDBA'),
            // 密码
            'password'        => env('database.password', 'SYSDBA'),
            // 连接参数
            'params'          => [],
            // 数据库编码
            'charset'         => 'UTF-8',
            // 数据库表前缀
            'prefix'          => 'gk_',
            // 自动写入时间戳字段
            'auto_timestamp'  => 'datetime',
            // 断线重连
            'break_reconnect' => true,
        ],
    ],
];
```

### 5. 配置 .env 环境变量

在 `.env` 文件中设置数据库连接信息：

```ini
[DATABASE]
TYPE     = dm
HOSTNAME = 127.0.0.1
HOSTPORT = 5236
DATABASE = EXAM_SYSTEM
USERNAME = SYSDBA
PASSWORD = SYSDBA
PREFIX   = gk_
```

### 6. 使用示例

配置完成后，使用与 MySQL 完全相同的方式操作数据库：

```php
<?php

use think\facade\Db;

// 查询
$users = Db::table('users')->where('status', 1)->select();

// Model查询
use app\model\User;
$user = User::find(1);

// 插入
Db::table('logs')->insert([
    'action' => 'login',
    'ip'     => '127.0.0.1',
    'time'   => date('Y-m-d H:i:s'),
]);

// 批量插入
Db::table('logs')->insertAll([
    ['action' => 'view', 'ip' => '127.0.0.1', 'time' => date('Y-m-d H:i:s')],
    ['action' => 'edit', 'ip' => '127.0.0.1', 'time' => date('Y-m-d H:i:s')],
]);

// 更新
Db::table('users')->where('id', 1)->update(['status' => 0]);

// 删除
Db::table('logs')->where('create_time', '<', '2025-01-01')->delete();

// 事务（支持嵌套Savepoint）
Db::transaction(function () {
    Db::table('orders')->insert($orderData);
    Db::table('order_items')->insertAll($items);
});
```

## 驱动特性

### 编码自动转换（UTF-8 ↔ GBK）

驱动在以下层面自动处理编码转换，确保中文数据正确读写：

| 方向 | 处理位置 | 说明 |
|------|---------|------|
| 写入 (UTF-8→GBK) | `getPDOStatement()` | INSERT/UPDATE/DELETE 参数自动转 GBK |
| 读取 (GBK→UTF-8) | `query()` / `pdoQuery()` / `column()` | 查询结果自动转 UTF-8 |

> 适用于 DM 数据库内部存储字符集为 GBK、PHP 源码为 UTF-8 的场景。

### 达梦适配特性

| 特性 | 说明 |
|------|------|
| **Schema 自动切换** | 连接后自动执行 `SET SCHEMA` 到配置的数据库 |
| **双引号标识符** | DM 使用双引号（`"column"`）代替 MySQL 反引号 |
| **系统视图支持** | `getFields()`/`getTables()` 通过 DM 系统视图获取元数据 |
| **主键识别** | 从 `ALL_CONSTRAINTS`/`ALL_CONS_COLUMNS` 获取主键 |
| **自增列识别** | 从 `SYSCOLUMNS.INFO2` 检测 IDENTITY 列 |
| **IN 子句整数字段修复** | 自动将 IN 子句中的值转为整数，避免 DM 字符串/整数匹配失败 |
| **事务嵌套** | 支持 Savepoint 事务嵌套 |
| **FIND_IN_SET** | 兼容 MySQL FIND_IN_SET 函数 |
| **REGEXP** | 兼容 MySQL REGEXP 正则查询 |

### DM8 兼容模式下 SQL 差异处理

- `INSERT` 使用标准 `INSERT INTO ... (cols) VALUES (...) ` 语法（DM 不支持 MySQL 的 `INSERT ... SET` 语法）
- JOIN ON 子句中的标识符自动加双引号
- 表名不加引号，内联别名加双引号，与 DM 大小写折叠规则保持一致

## 已知限制

1. **字符集**: 假设数据库存储为 GBK，应用代码为 UTF-8。若数据库本身为 UTF-8，需要修改 `getPDOStatement()` 和 `convertResultEncoding()` 中的编码转换逻辑
2. **ON DUPLICATE KEY**: DM 原生不支持 MySQL 的 `ON DUPLICATE KEY UPDATE` 语法，当前适配的是 MySQL 兼容模式下的近似行为
3. **JSON 函数**: 通过 `json_extract` 模拟 MySQL 的 `->` 操作符
4. **`ATTR_EMULATE_PREPARES`**: 默认开启客户端模拟预处理（`PDO::ATTR_EMULATE_PREPARES = true`），因为 DM PDO 驱动原生预处理对 DELETE/IN 子句存在 bug

## License

Apache-2.0
