# Hhttp

**用 JavaScript 写业务逻辑的 HTTP / WebSocket 服务器**（C++17 + Boost.Asio + OpenSSL + QuickJS）

**版本 1.1（首个正式版）**

网络层（TCP、TLS、HTTP 解析、RFC 6455 WebSocket）全部由 C++ 实现，业务逻辑交给 JS 脚本：
配置里每条路由绑定一个 `.js` 文件，脚本通过 `HTTP.get` / `HTTP.send` / `ws` / `File` / `Sqlite` /
`Cookie` 完成请求处理。改脚本即改逻辑，不需要重新编译，也没有 npm 依赖。

> Hhttp is a small C++17 HTTP/1.1 + WebSocket server that maps routes to QuickJS scripts.
> Network and TLS are native; application logic lives in plain JavaScript files.

---

## 特性

| | |
| --- | --- |
| **HTTP/1.1** | 请求行 / 请求头 / 请求体完整解析；查询串与 Cookie 自动解码；Keep-Alive、流水线、HEAD |
| **响应** | 定长、`Transfer-Encoding: chunked`、定长流式、SSE、大文件下载（`res.file()`） |
| **WebSocket** | RFC 6455 服务端：握手、掩码校验、分片重组、Ping/Pong、Close（支持自定义关闭码） |
| **HTTPS / WSS** | OpenSSL 3.x，PFX 或 PEM 证书；一个端口挂多张证书，按 SNI 自动选择；TLS 1.2 / 1.3 |
| **路由** | 域名路由（虚拟主机）、默认域名表、`*.example.com` 通配子域、前缀匹配、兜底处理器 |
| **脚本沙箱** | 每个脚本独立的文件读写白名单、SQLite 白名单；越界路径与 `..` 一律拒绝 |
| **脚本能力** | `HTTP.get` / `HTTP.send`、`File`（分块 / 按行读）、`Sqlite`、`Cookie`、`ws`、`console` |
| **中间件** | 请求过滤器（安全检测脚本）：IP 黑名单、鉴权、限流，fail-closed |
| **全局脚本** | 常驻运行时 + `Global.call()` / `Global.set()`，跨请求共享数据 |
| **防护** | 请求行 / 头 / 体上限与总超时、请求走私校验、响应头注入清洗、日志注入清洗、脚本内存上限 |
| **日志** | 异步有界队列、按日期落盘、访问日志单独分流、可选彩色控制台输出 |
| **跨平台** | Windows（IOCP）与 Linux（epoll）同一份源码，行为一致；macOS 代码就绪 |

性能取向：QuickJS 解释执行 + C++ 文本解析，Release（`-O2`）下同机实测
`/static/` 约 7k req/s、404 路径约 62k req/s。

---

## 快速开始

### 1. 依赖

| 依赖 | 版本 | 说明 |
| --- | --- | --- |
| C++ 编译器 | GCC 11+ / Clang / MSVC | 项目使用 C++17 |
| CMake | ≥ 3.16 | 推荐搭配 Ninja |
| [Boost](https://www.boost.org/) | 1.74+ | 只用头文件（Asio / System） |
| [OpenSSL](https://www.openssl.org/) | 3.x | 系统包、vcpkg 或自编译静态库均可 |
| [QuickJS](https://github.com/quickjs-ng/quickjs) | quickjs-ng 或原版 | 需要 `quickjs.h` + `libquickjs.a` |
| [SQLite3](https://sqlite.org/) | 3.x | 系统包或静态库 |

CMake 会先找缓存变量 `HHTTP_BOOST_DIR` / `HHTTP_OPENSSL_DIR` / `HHTTP_QUICKJS_DIR` /
`HHTTP_SQLITE3_DIR` 指向的目录，找不到时自动回退到 `find_package` / `find_path`。
各依赖的获取与编译方式见 [用户手册 · 13.2](docs/用户手册.md#132-依赖与版本)。

### 2. 构建

Linux / macOS（Boost / OpenSSL / SQLite3 已安装到系统路径；QuickJS 需自行编译，
用 `-DHHTTP_QUICKJS_DIR` 指向它，或安装到系统 include / lib 路径）：

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build -j
```

Windows（MinGW-w64，依赖放在自定义目录）：

```powershell
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release `
  -DHHTTP_BOOST_DIR=A:/libs/boost_1_92_0 `
  -DHHTTP_OPENSSL_DIR=A:/libs/openssl `
  -DHHTTP_QUICKJS_DIR=A:/libs/quickjs `
  -DHHTTP_SQLITE3_DIR=A:/libs/sqlite3
cmake --build build
```

产物为 `build/Hhttp.exe`（Linux 为 `build/Hhttp`），默认 Release。
MinGW 下默认静态链接全部依赖与运行时，拷一个 exe 即可部署。
也可以使用预设：`cmake --preset release` / `debug` / `relwithdebinfo`（需要 CMake ≥ 3.23）。

### 3. 运行

```powershell
# Windows,在仓库根目录执行
.\build\Hhttp.exe --config config.example.json
```

```bash
# Linux / macOS
./build/Hhttp --config config.example.json
```

打开 <http://127.0.0.1:8080/> 可以看到示例页面，或直接验证：

```bash
curl -i http://127.0.0.1:8080/
curl -i http://127.0.0.1:8080/api/time
```

`config.example.json` 配置了两条路由：

| 路由 | 处理器 | 行为 |
| --- | --- | --- |
| `/`（前缀，任意 Host） | [scripts/hello.js](scripts/hello.js) | 返回自包含的示例页面；`/api/time` 返回 JSON；`/api/echo` 回显请求 |
| `/ws` | [scripts/ws_echo.js](scripts/ws_echo.js) | WebSocket 回显：文本回 `echo: ...`，二进制原样回送 |

---

## 用 JavaScript 写业务

```js
// scripts/hello.js 的核心几行
const req = HTTP.get;    // 当前请求:method()、url()、query()、headers()、body()、cookie() ...
const res = HTTP.send;   // 待发送的响应:status()、header()、json()、html()、file()、send() ...

res.status(200);
res.header("X-Powered-By", "Hhttp");
res.html("<h1>Hello Hhttp</h1>");
res.send();              // HTTP 脚本必须显式调用 send()
```

WebSocket 脚本拿到的是 `ws` 对象，可以写阻塞式循环：

```js
// scripts/ws_echo.js
ws.send("welcome, " + ws.peer());
while (ws.valid()) {
    const msg = ws.recv(1000);      // 超时返回 undefined,关闭返回 null
    if (msg === undefined) continue;
    if (msg === null) break;
    ws.send("echo: " + msg);
}
```

脚本在每次请求时重新加载，改完立即生效。完整的 API（`HTTP.get` / `HTTP.send` / `File` /
`Sqlite` / `Cookie` / `console` / `ws` / `Global`）见
[用户手册 · JavaScript 脚本 API](docs/用户手册.md#6-javascript-脚本-api)。

---

## 配置

配置文件是一份 JSON（**不支持注释**），由三部分组成：

```json
{
  "base_msg": {
    "HTTP_port": 8080,
    "HTTPS_port": 0,
    "pfx_path": "",
    "pfx_password": "",
    "script_dir": "scripts"
  },
  "roter": [
    { "/ws": { "websocket": { "js_path": "ws_echo.js" } } },
    { "/":   { "http":      { "js_path": "hello.js" } } }
  ],
  "undefine_roter": {
    "http": { "js_path": "" }
  }
}
```

- `base_msg`：监听端口、证书（PFX 或 PEM / 多证书 SNI）、脚本目录、超时与内存上限、安全脚本与全局脚本。
- `roter`：路由表，键是 `"域名/路径"`（或 `"/路径"` 表示任意 Host）；每条路由可同时有 `http` 与 `websocket` 处理器。
- 每个处理器可单独授予权限：`js_read_rule` / `js_write_rule`（目录）、
  `js_sql_read_rule` / `js_sql_write_rule`（SQLite 文件），或 `js_full_access`（高危）。
- `undefine_roter`：没有匹配到可用处理器时的兜底行为，不配置则返回 404。

完整字段说明、路由匹配规则与权限模型见
[用户手册 · 配置文件参考](docs/用户手册.md#5-配置文件参考)。

命令行参数（用 `--help` 查看全部）：

```
--config <path>, -c <path>     配置文件（默认 config.json）
--dir <path>                   脚本目录（默认配置里的 script_dir，否则 scripts）
--file-max-size <bytes>        脚本单次读取上限（默认 8 MiB）
--js-memory-limit <bytes>      业务脚本内存上限（默认 64 MiB,0 = 不限制）
--js-security-memory-limit ... 安全脚本内存上限（默认 64 MiB）
--js-global-memory-limit ...   全局脚本内存上限（默认 128 MiB）
--help, -h                     打印用法
```

---

## 仓库结构

```text
.
├─ CMakeLists.txt            构建脚本（依赖查找与回退、平台分支、静态链接）
├─ CMakePresets.json         release / debug / relwithdebinfo 预设
├─ config.example.json       可直接运行的示例配置
├─ src/                      服务器源码
│  ├─ main.cpp               入口：命令行、配置加载、路由注册、监听
│  ├─ TCP.h / .cpp           连接与监听（Boost.Asio 之上的阻塞 facade）
│  ├─ TLS.h / .cpp           OpenSSL 服务端 TLS：PFX/PEM、SNI、握手
│  ├─ HTTP.h / .cpp          HTTP 解析与响应、路由、过滤器、分发器、访问日志
│  ├─ WebSocket.h / .cpp     RFC 6455 服务端
│  ├─ JS.h / .cpp            QuickJS 集成：HTTP / ws / File / Sqlite / Cookie / Global
│  └─ Log.h / .cpp           异步日志
├─ third_party/nlohmann/     单头文件 JSON 库（MIT）
├─ scripts/                  默认脚本目录
│  ├─ hello.js               HTTP 示例
│  ├─ ws_echo.js             WebSocket 示例
│  └─ examples/              安全脚本、全局脚本示例
├─ tests/                    PowerShell 回归测试（85 + 21 + 21 条）
├─ docs/                     用户手册
└─ LOG/                      运行时自动创建的日志目录（已 gitignore）
```

---

## 示例脚本

- **最小示例**：`scripts/hello.js`、`scripts/ws_echo.js`，由 `config.example.json` 直接引用。
- **安全脚本 / 全局脚本示例**：`scripts/examples/security.js`、`scripts/examples/global.js`，
  把 `base_msg.js_security_script` / `base_msg.js_global_script` 指向它们即可启用。

---

## 测试

回归测试用 PowerShell 编写（Windows PowerShell 5.1 与 PowerShell 7 均可运行），覆盖 HTTP 解析与安全边界、
Keep-Alive、流水线、chunked、文件与 SQLite 权限、响应头注入、Cookie、WebSocket、
TLS/SNI/PEM 与路由分发。先构建，然后在仓库根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File tests\run-tests.ps1           # 85 条:HTTP / WS / 脚本 / 安全
powershell -ExecutionPolicy Bypass -File tests\run-routing-tests.ps1   # 21 条:路由分发
powershell -ExecutionPolicy Bypass -File tests\run-tls-tests.ps1       # 21 条:HTTPS / WSS / SNI / PEM
```

测试脚本会自己拉起服务、跑完关闭，退出码为失败条数（0 = 全部通过）。
`-Exe <path>` 可指定被测可执行文件，`-NoStart` 可对已运行的服务做回归。
本仓库的回归状态：**85 + 21 + 21 全部通过**（Windows x64，GCC 16.2）。

---

## 文档

- [用户手册](docs/用户手册.md) —— 完整参考：构建、配置、JavaScript API、C++ API、运行时行为、
  安全实践、FAQ、已知限制、跨平台部署。

## 平台支持

| 平台 | 状态 |
| --- | --- |
| Windows 10 / 11 x64（MinGW-w64 GCC 16.2） | 构建 + 全部回归通过 |
| Linux aarch64（openEuler 24.03，GCC 12.3） | 构建 + 85 + 21 条回归通过 |
| Linux x86_64 / macOS | 代码就绪；macOS 未实机验证 |

## 安全

脚本是可信代码：它按配置获得文件与 SQLite 权限，不要把上传文件、动态生成脚本作为业务输入。
生产环境建议：使用 HTTPS、最小化文件白名单、关闭 `js_full_access`、开启访问日志并定期归档。
详见 [用户手册 · 安全实践](docs/用户手册.md#10-安全实践)。

发现安全问题请**不要**直接开公开 issue，按 [SECURITY.md](SECURITY.md) 的方式私下联系。

## 贡献

欢迎 issue 与 PR。开发约定、构建与测试流程见 [CONTRIBUTING.md](CONTRIBUTING.md)。
提交前请先跑一遍 `tests/` 下的三套回归。

## 许可证

[Apache License 2.0](LICENSE) © 2026 Hhttp contributors

项目名称与版权信息见 [NOTICE](NOTICE)。

### 第三方组件

| 组件 | 许可证 | 使用方式 |
| --- | --- | --- |
| [nlohmann/json](https://github.com/nlohmann/json) | MIT | `third_party/nlohmann/json.hpp`（仓库自带） |
| [Boost.Asio / System](https://www.boost.org/) | Boost Software License 1.0 | 编译期头文件依赖 |
| [OpenSSL](https://www.openssl.org/) | Apache-2.0 | 链接依赖 |
| [QuickJS](https://github.com/quickjs-ng/quickjs) | MIT | 链接依赖（需自行编译） |
| [SQLite](https://sqlite.org/) | Public Domain | 链接依赖 |
