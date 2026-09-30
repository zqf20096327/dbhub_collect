# TarsCloud-OB

基于 [TarsCloud/Tars](https://github.com/TarsCloud/Tars) 的 OceanBase 适配版本。

## 版本信息

| 组件 | 版本 | 上游仓库 | 日期 |
|---|---|---|---|
| TarsFramework | v3.0.17 | [TarsCloud/Tars](https://github.com/TarsCloud/Tars) | 2024-02-02 |
| TarsCpp (tarscpp) | v3.0.19 | [TarsCloud/TarsCpp](https://github.com/TarsCloud/TarsCpp) | 2024-02-02 |
| TarsWeb | v3.0.15 | [TarsCloud/TarsWeb](https://github.com/TarsCloud/TarsWeb) | 2024-02-02 |

## 说明

本版本在上游 TarsCloud 的基础上做了以下定制：

- **数据库后端适配**：将 MySQL 替换为 OceanBase MySQL 租户模式
- **mysql-tool 重写**：用 Node.js 版本替换原有 C++ 版 mysql-tool，兼容 OceanBase 语法差异
- **离线部署支持**：自包含 Node.js 运行时、npm 依赖及预编译二进制，无需外网

## 相关文档

- [安装手册](INSTALL.md)
- [部署运维手册](TarsCloud_部署运维手册.md)
- [TarsCloud 官方文档](https://tarscloud.github.io/TarsDocs)
