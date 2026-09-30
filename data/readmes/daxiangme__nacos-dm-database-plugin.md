This project provides a Dameng (DM) database plugin for Nacos 3.1.2,
allowing Nacos to run on 国产数据库达梦 (DM Database) instead of MySQL.
Supports:
- Nacos 3.1.2
- DM8 (达梦数据库)

# Nacos 达梦数据库插件（3.1.2）


## ✨ Features
- 支持 Nacos 3.1.2
- 支持 达梦 DM8
- 替代 MySQL

## 🚀 Quick Start
### 1. 克隆代码
```bash
git clone https://github.com/<your-org>/nacos-plugin-3.1.2.git
cd nacos-plugin-3.1.2
```

### 2. 进入 `nacos-datasource-plugin-ext` 并打包
```bash
cd nacos-datasource-plugin-ext
mvn -pl nacos-dm-datasource-plugin-ext -am clean package -DskipTests
```

### 3. 拷贝插件到 Nacos `plugins` 目录
```bash
# Linux / macOS
cp nacos-dm-datasource-plugin-ext/target/*.jar $NACOS_HOME/plugins/

# Windows PowerShell
Copy-Item .\nacos-dm-datasource-plugin-ext\target\*.jar "$env:NACOS_HOME\plugins\"
```

## 🔧 Configuration
在 Nacos `application.properties` 中配置达梦数据源：

```properties
spring.datasource.platform=dm
db.url.0=jdbc:dm://127.0.0.1:5236/DMSERVER?schema=NACOS&compatibleMode=mysql&ignoreCase=true&ENCODING=utf-8
db.user.0=SYSDBA
db.password.0=SYSDBA
db.pool.config.driverClassName=dm.jdbc.driver.DmDriver
```

初始化表结构（首次部署）：

`nacos-datasource-plugin-ext/nacos-dm-datasource-plugin-ext/schema/nacos-dm.sql`

如果你的 schema 不是 `NACOS`，请先按实际 schema 名称修改 SQL 后再执行。

## 📦 Compatibility
| Nacos | DM |
|------|----|
| 3.1.2 | DM8 |

## ❓ Why this project
很多国产化部署场景要求数据库不使用 MySQL，而 Nacos 默认以 MySQL 生态为主。  
这个插件提供 Nacos 3.1.2 对达梦 DM8 的适配能力，帮助你在国产数据库环境中平滑落地。

## 🔍 Keywords
Nacos 达梦数据库插件, Nacos DM Plugin, 国产数据库适配

## 相关模块
- [数据源插件集合](./nacos-datasource-plugin-ext)
- [达梦插件模块](./nacos-datasource-plugin-ext/nacos-dm-datasource-plugin-ext)
- [其他扩展插件](./nacos-config-change-plugin-ext)
