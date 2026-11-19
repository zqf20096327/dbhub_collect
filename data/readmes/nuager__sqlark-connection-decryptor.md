# SQLark 连接解密工具（sqlark-connection-decryptor）

**简体中文** · [繁體中文](README.zh-TW.md) · [English](README.en.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Русский](README.ru.md) · [Português (BR)](README.pt-BR.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](#)
[![CI](https://github.com/muemios/sqlark-connection-decryptor/actions/workflows/ci.yml/badge.svg)](../../actions/workflows/ci.yml)

解析 **SQLark（百灵）** 保存的数据库连接文件（`connectionInfo.xml` /
`connection-server.xml`），批量还原其中加密保存的数据库密码。

> [!WARNING]
> 本工具仅用于**本机凭据找回、密码审计与安全自查**，例如：忘记自己保存的数据库密码、
> 迁移机器前导出连接、评估 SQLark 本地凭据存储强度。
> 请勿用于未经授权的他人计算机或数据库，由此产生的一切后果由使用者自行承担。
> 详见 [SECURITY.md](SECURITY.md)。

> [!NOTE]
> 本项目为非官方社区项目，与 SQLark / 达梦（DM）官方无关联，也未获其背书。

---

## 功能特性

- **自动检索**：自动发现 `~/.SQLark`、`%APPDATA%\SQLark`、桌面/文档/下载以及各磁盘 SQLark 安装目录中的连接文件；
- **手动指定**：支持选择目录（递归查找）或直接选择文件；
- **批量解密**：一次解析全部连接，还原用户名、地址、端口、数据库类型与明文密码；
- **图形界面 + 命令行**：Tkinter GUI 适合日常使用，CLI 适合脚本化处理；
- **导出**：CSV（Excel 直接打开不乱码）、TXT、JSON；
- **纯本地运行**：不联网、不上传、不写注册表，只读取你指定的文件；
- **可打包**：一条命令构建免安装的 Windows 单文件 exe。

![GUI 截图](docs/images/gui-demo.png)

> 截图中的主机、用户名、密码均为演示数据（RFC 5737 文档专用网段）。

---

## 快速开始

### 方式一：下载 exe（推荐普通用户）

到 [Releases](../../releases) 下载 `sqlark-connection-decryptor-v*-windows-x64.exe`，双击运行即可（无需安装 Python）。
需要命令行/脚本化调用时，下载 `sqlark-connection-decryptor-cli-v*-windows-x64.exe`（控制台版）。

发布产物按平台/架构命名：
- Windows x64（图形界面）：`sqlark-connection-decryptor-v*-windows-x64.exe`
- Windows x64（命令行）：`sqlark-connection-decryptor-cli-v*-windows-x64.exe`
- Linux x64（命令行）：`sqlark-connection-decryptor-cli-v*-linux-x64.tar.gz`
- Linux arm64（命令行）：`sqlark-connection-decryptor-cli-v*-linux-arm64.tar.gz`
- macOS（命令行）：`sqlark-connection-decryptor-cli-v*-macos-arm64.tar.gz`（Apple Silicon）、`sqlark-connection-decryptor-cli-v*-macos-x64.tar.gz`（Intel）

### 方式二：从源码运行

```bash
git clone https://github.com/muemios/sqlark-connection-decryptor.git
cd sqlark-connection-decryptor
pip install -e .            # 或 pip install -r requirements.txt
python -m sqlark_decrypt    # 启动图形界面
```

### 方式三：命令行

```bash
# 自动检索并打印全部连接
python -m sqlark_decrypt scan --auto

# 解密单个文件
python -m sqlark_decrypt decrypt "C:\Users\me\.SQLark\connectionInfo.xml"

# 批量解密 + 导出
python -m sqlark_decrypt decrypt "*.xml" --csv result.csv --txt result.txt --json result.json
```

输出示例：

```
连接名            主机             端口    用户名          数据库         密码
--------------------------------------------------------------------------
demo-oracle    192.0.2.10     1521  demo_user    ORACLE      Demo#Pass123
demo-mysql     198.51.100.24  3306  demo_reader  MYSQL       ReadOnly!2024
demo-postgres  203.0.113.5    5432  analyst      POSTGRESQL  analyst_pw
```

### 构建可执行文件（跨平台）

统一使用 `scripts/build_binary.py`，产物自动带平台/架构后缀：

```bash
python scripts/build_binary.py --variant cli   # 本机平台命令行版
```

Windows 图形界面版：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/build_exe.ps1
# 产物: dist\sqlark-connection-decryptor-v*-windows-x64.exe
```

---

## 支持的连接文件

| 文件 | 说明 |
| --- | --- |
| `%USERPROFILE%\.SQLark\connectionInfo.xml` | SQLark 本机全部连接（最常见） |
| 任意导出的 `connection-server.xml` | “导出连接”生成的单个/多个连接 |
| `connections.xml` 等其他导出名 | 只要根节点是 `<CONNECTIONS>` 即可识别 |

兼容性：在 **SQLark 4.x（Oracle / MySQL / PostgreSQL / 达梦等驱动）** 上验证通过。
加密实现来自 SQLark 的 Java 后端 jar，若官方更换算法，本工具会解析失败而不是给出错误密码。

---

## 工作原理（简述）

SQLark 对连接信息做了**两层 AES-128-CBC（PKCS5Padding）**：

1. **外层**：整个 `<connectionDetail>` / `<superAttr>` 字段
   `Base64(AES(JSON, key="fudih4xp113znwp7", iv=reverse(key)))`
2. **内层**：JSON 中的 `password` / `sshPassword` / `sslPassword`
   `Base64(AES(明文, key=salt, iv=reverse(salt)))`，`salt` 为该连接随机生成的 16 位字符串，与密文存放在同一 JSON 中。

完整逆向过程、代码出处与安全性分析见 [docs/encryption.md](docs/encryption.md)。

---

## 项目结构

```
sqlark-decryptor/
├── sqlark_decrypt/          # 可复用 Python 包
│   ├── crypto.py            # 双层 AES 加解密原语（无业务逻辑）
│   ├── models.py            # ConnectionRecord 数据模型
│   ├── parser.py            # XML 解析 + 组合两层解密
│   ├── scanner.py           # 磁盘检索（自动发现 / 递归扫描）
│   ├── export.py            # CSV / TXT / TSV / JSON 导出
│   ├── cli.py               # 命令行：gui / scan / decrypt
│   ├── gui.py               # Tkinter 图形界面
│   └── __main__.py          # python -m sqlark_decrypt 入口
├── tests/                   # pytest 单元测试（含脱敏测试夹具）
├── scripts/                 # 构建、演示数据、图标、敏感信息自检
├── docs/                    # 加密原理、架构、开发与发布文档
├── assets/                  # 图标等静态资源
├── .github/workflows/       # GitHub Actions CI
└── pyproject.toml           # 打包与工具配置
```

各模块职责与数据流见 [docs/architecture.md](docs/architecture.md)。

---

## 开发

```bash
pip install -e ".[dev]"

pytest                          # 运行单元测试
ruff check .                    # 代码风格检查
python scripts/check_no_secrets.py   # 提交前敏感信息自检
python scripts/check_i18n.py         # 多语言 README 一致性检查
```

- 测试夹具 `tests/fixtures/demo-connections.xml` 由 `scripts/make_fixture.py` 生成，
  内容全部为虚构数据（文档专用网段 + 演示密码）。
- 贡献指南见 [CONTRIBUTING.md](CONTRIBUTING.md)，发布流程见 [docs/development.md](docs/development.md)。

---

## 隐私与数据安全

- 程序**不联网**、不上传任何数据、不修改 SQLark 文件；
- 解密结果可能包含**生产数据库密码**：请勿把导出的 CSV/JSON 提交到 Git、网盘或聊天工具；
- 仓库内已配置 `.gitignore` 忽略真实连接文件，并提供 `scripts/check_no_secrets.py` 与 CI 检查，防止误提交。

---

## 常见问题

**Q：自动检索没有结果？**
A：点击「② 选择目录」，选择 `C:\Users\<你>\.SQLark` 或导出文件所在目录。

**Q：密码列是空的？**
A：该连接保存时未勾选“记住密码”，文件中没有密文。

**Q：解析失败 / 密码不对？**
A：SQLark 升级可能更换加密方式。请提交 Issue 并附上 SQLark 版本号（**不要附真实连接文件**）。

**Q：Windows Defender 报毒？**
A：PyInstaller 打包的未签名 exe 常被误报，可自行从源码构建或添加信任。

---

## License

[MIT](LICENSE) © 2026 SQLark Decryptor contributors

---

## 关键词

SQLark 密码解密、SQLark 百灵 密码找回、数据库连接密码恢复、Oracle / MySQL / PostgreSQL / 达梦 保存密码、AES-128-CBC 逆向、凭据恢复、安全自查、Tkinter 桌面工具、离线密码审计、connectionInfo.xml 解密、connection-server.xml 解密。

---

## English Summary

A cross-platform tool that decrypts database connection files saved by **SQLark**
(`connectionInfo.xml` / `connection-server.xml`). SQLark encrypts connection details with a
two-layer AES-128-CBC scheme (fixed outer key + per-connection `salt`). This project parses the
XML, restores the plaintext passwords, and offers both a Tkinter GUI and a CLI. It is intended
for legitimate local credential recovery and security self-assessment only.

