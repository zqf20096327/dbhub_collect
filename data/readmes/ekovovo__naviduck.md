<div align="center">

<img src="crates/naviduck/icons/naviduck.png" alt="Naviduck" width="180"/>

# Naviduck

**用 Rust 复刻 Navicat Premium 17 的开源数据库 GUI**

[下载 Nightly](https://github.com/ekovovo/naviduck/releases/tag/nightly) · [设计文档](docs/design/00-overview.md) · [实现进度](docs/progress.md)

</div>

---

Naviduck 是一个以 macOS 优先的数据库图形客户端：用 [gpui-kit](https://crates.io/crates/gpui-kit) 从零复刻 Navicat Premium 17 的界面与交互，不依赖 Electron，也不 fork gpui-kit。

![screenshot](https://i.ibb.co/84Nj1Vz3/image-1.webp)

## 支持的数据库

| 数据库 | 连接 | 对象浏览 | 表查看器 | 查询编辑器 | 表设计器 |
| --- | :-: | :-: | :-: | :-: | :-: |
| MySQL / MariaDB | ✅ | ✅ | ✅ | ✅ | ✅ |
| PostgreSQL | ✅ | ✅ | ✅ | ✅ | ✅ |
| SQLite | ✅ | ✅ | ✅ | ✅ | ✅ |
| 达梦 DM8 | ✅ | ✅ | ✅ | ✅ | ✅（迁移不可回滚，见提示） |

连接方式：常规 / SSH 隧道（DM8 的 SSL 暂不支持）；连接配置文件、密码钥匙串存储、连接组与颜色。

## 主要功能

- **对象浏览**：数据库 → 模式 → 表/视图/函数/过程/序列/触发器，含系统对象开关、筛选、右键菜单与详情视图
- **表查看器**：分页网格、单元格编辑（文本/十六进制/JSON/枚举编辑器）、原始数据模式、事务、外键取值、筛选与排序、查找替换
- **查询编辑器**：语法高亮、代码补全（关键字/字段/别名）、格式化、多结果集、参数、解释视图、命令列、历史日志
- **表设计器**：字段/索引/外键/检查/选项的结构化表单、SQL 预览、差异迁移（MySQL 原地 ALTER、PG/SQLite 事务内重建、DM 逐条执行）
- **定义设计器**：视图/函数/过程/序列/触发器/表空间等对象的新建与编辑
- **安全与工具**：用户/角色/权限管理（按数据库能力而定）、服务器监控、在库中查找
- **应用层**：浅色/深色外观、中英双语、收藏夹、启动画面、代码段、查询保存与自动恢复、应用内更新

## 下载

到 [Releases](https://github.com/ekovovo/naviduck/releases) 获取安装包：

- **Nightly**（预发布）：`Naviduck-aarch64.dmg` 等，每日构建，跟随 main
- 安装包附 `SHA256SUMS`；应用内「检查更新」读取同一清单

> Nightly 构建未做正式签名与公证，macOS 首次打开可能需要在系统设置中放行。

## 本地构建

```sh
# 需要 Rust 1.99（见 rust-toolchain.toml）与 Xcode
cargo build -p naviduck
cargo run -p naviduck
```

单元测试与 headless UI 测试：

```sh
cargo test --workspace
```

实库测试（MySQL 8 / MariaDB 11 / PostgreSQL 16，由 docker compose 提供）：

```sh
docker compose up -d --wait
NAVIDUCK_LIVE=1 cargo test -p naviduck-db -p naviduck-schema -p naviduck-query --lib --test live --locked
docker compose down
```

达梦 DM8 实库测试为本地可选（DM 开发版许可限定学习/测试/开发用途，不进 CI），启动方式见 [`crates/naviduck-dameng/tests/live.rs`](crates/naviduck-dameng/tests/live.rs) 文件头。

> 达梦驱动使用 [`dm-pure`](https://crates.io/crates/dm-pure)（MIT，纯 Rust）。1.2.4 有四处协议缺陷（LOB/EXPLAIN/SET SCHEMA/错误消息前缀），上游仓库已失效；修复补丁的托管与接线在推进中（见 [验收记录](docs/pr/acceptance-dameng.md)），当前版本使用 crates.io 原版，实库测试对相关行为自动跳过。

## 项目结构

工作区按依赖方向拆分 crate（见 [00-overview](docs/design/00-overview.md)）：`naviduck-model`（纯数据）、`naviduck-db`（驱动契约与运行时）、`naviduck-sql`（方言与词法）、每种数据库一个 `naviduck-<db>` crate、`naviduck-session`/`naviduck-app-state`（会话与状态）、`naviduck-*` 界面 crate；外壳 `crates/naviduck` 组合窗口与面板。核心层不依赖 GPUI，`scripts/check-deps.sh` 在 CI 检查。

## 许可

Apache-2.0。第三方图标版权见各 SVG 文件头注释（Tabler Icons、Devicon）；Naviduck 图标为本项目原创图形。
