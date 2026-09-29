# tidb_sm3_password — MySQL 客户端 SM3 国密认证插件

基于 MySQL CLI 的客户端插件机制实现，使用 SM3 国密算法（GB/T 32905-2016）
完成认证。协议完全对齐 `caching_sha2_password`，仅将哈希函数从 SHA-256 替换为
SM3；服务端（TiDB `tidb_sm3_password` 插件）同样按 caching_sha2_password 的
方式实现。

```
scramble = SM3(password) XOR SM3(salt + SM3(SM3(password)))
```

## 功能

- 客户端认证插件，通过 `--default-auth=tidb_sm3_password` 选择性加载；
- 插件名与服务端一致（`tidb_sm3_password`），也支持服务端
  AuthSwitchRequest 按名匹配自动加载（无需 `--default-auth`）；
- 兼容 MySQL 5.7 / 8.0 / 9.0 客户端（详见下文 ABI 说明）；
- 安全策略与上游 `caching_sha2_password` 一致：仅允许在 TLS 安全通道上发送
  明文密码，非 TLS 连接在 full-auth 阶段拒绝发送密码（ERROR 2061）。

## 目录结构

```
.
├── src/
│   ├── sm3.h / sm3.c              # 自包含 SM3 实现（无外部加密库依赖）
│   ├── sm3_scramble.h/.c          # SM3 scramble 计算
│   └── tidb_sm3_password.c        # 客户端认证插件（多 ABI 自适应）
├── include/
│   ├── 5.7/                       # 5.7.44 公共头文件（vendored，GPL）
│   └── 8.0.26/                    # 8.0.26 公共头文件（vendored，GPL）
├── build/                         # 构建产物（按 平台/架构/客户端版本 组织）
│   ├── macos/x86_64/<版本>/       #   Intel Mac（Mach-O x86_64）
│   ├── macos/aarch64/<版本>/      #   Apple Silicon（Mach-O arm64）
│   ├── linux/x86_64/<版本>/       #   Linux/Docker amd64（ELF）
│   ├── linux/aarch64/<版本>/      #   Linux/Docker arm64（ELF）
│   └── windows/x86_64/<版本>/     #   Windows（PE DLL，附 .pdb）
├── build.sh                       # 统一编译脚本（自动适配平台/架构，zig 交叉编译）
├── test/
│   ├── sm3_test.c                 # 离线单测（SM3 向量/scramble/ABI）
│   ├── plugin_flow_test.c         # mock VIO 认证流程测试（各 ABI）
│   ├── connect_test.sh            # 真实连接测试（本机）
│   └── docker_test.sh             # mysql:5.7 容器内连接测试
└── Makefile
```

## 编译

依赖：C 编译器；现代目标（8.0.27+/9.x）需要 MySQL 客户端 SDK 头文件
（默认 `MYSQL_HOME=/usr/local/mysql`，可用 `make MYSQL_HOME=<path>` 覆盖，
例如 `$(brew --prefix mysql-client)`）。5.7 / 8.0.26 头文件已随仓库提供。

```bash
./build.sh            # 本机构建（自动识别宿主机平台/架构）
./build.sh all        # 全矩阵：macos+linux+windows × x86_64+aarch64
./build.sh linux      # 交叉编译 Linux（架构默认取宿主机）
./build.sh windows    # 交叉编译 Windows DLL
make test             # 离线单测 + 各 ABI 流程测试
make connect          # 真实连接测试（需要运行中的服务端）
```

各平台产物格式不同（Mach-O / ELF / PE DLL），不能混用。`./build.sh` 自动识别
构建环境（`uname -s`/`uname -m`），本机构建用系统编译器，交叉构建用 zig（首次
自动下载到 `zig-dist/`，已加入 .gitignore）。产物目录统一为
`build/<os>/<arch>/<客户端版本>/`。

## 使用

```bash
# 方式一：--default-auth 显式加载（推荐）
mysql --plugin-dir=/path/to/build/8.0.27+ \
      --default-auth=tidb_sm3_password \
      -h 127.0.0.1 -P 4000 -u user03 -p

# 方式二：不指定 --default-auth，服务端 AuthSwitchRequest 按名匹配自动加载
mysql --plugin-dir=/path/to/build/8.0.27+ \
      -h 127.0.0.1 -P 4000 -u user03 -p
```

> `--plugin-dir` 指向与客户端版本匹配的构建目录。macOS 上插件文件为
> `tidb_sm3_password.so`（客户端同时尝试 `.dylib` 与 `.so`），Linux 同。

### 与客户端版本的对应关系

| 客户端版本        | 插件接口版本 | 使用 build 目录           |
|-------------------|--------------|---------------------------|
| MySQL 5.7.x       | 0x0100       | `.../5.7/`                |
| MySQL 8.0.0–8.0.10（开发版） | 0x0100 | `.../8.0.0-8.0.10/` |
| MySQL 8.0.11–8.0.26 | 0x0100/0x0101 | `.../8.0.11-8.0.26/` |
| MySQL 8.0.27+     | 0x0200       | `.../8.0.27+/`            |
| MySQL 8.4 / 9.x   | 0x0200       | `.../8.0.27+/`            |

> 注意：8.0.0–8.0.10 是 2018 年左右的开发里程碑版本，其 `MYSQL` 结构体布局
> 与 8.0.11+ 正式版不同（`MYSQL.passwd` 偏移 704 vs 688），必须使用
> `8.0.0-8.0.10/` 目录下的独立构建（例如 docker 镜像 `mysql:8.0.0`）。
> 实际使用中请优先选择 8.0.27+ 的正式版客户端镜像。

## ABI 说明（为什么需要三个构建）

客户端插件描述符（`_mysql_client_plugin_declaration_`）的布局随客户端版本
变化：

- 5.7、8.0.0–8.0.10：无 `get_options`，无 `authenticate_user_nonblocking`；
- 8.0.11–8.0.26：仍无 `get_options`，但新增 `authenticate_user_nonblocking`；
- 8.0.27+ / 9.x：新增 `get_options`，接口版本升到 0x0200。

客户端加载时的版本检查为 `interface_version >= 期望值 且主版本相同`，因此
低版本插件无法加载到新客户端，反之亦然；同时 `MYSQL`/`NET` 结构体字段偏移
在 5.7 与 8.0 之间不同，必须用对应版本的 SDK 头文件编译。三者共用同一份
插件源码，仅描述符声明与头文件不同（由 `MYSQL_VERSION_ID` 自动选择）。

## 认证流程

1. 客户端连接，服务端握手（默认插件为 `mysql_native_password`）；
2. 服务端对 `tidb_sm3_password` 账户发送 AuthSwitchRequest
   （插件名 + 20 字节盐值）；
3. 客户端插件计算并发送 32 字节 SM3 scramble；
4. 服务端回复 `0x04`（perform full authentication，本服务端未实现快速认证
   缓存，总是走完整认证）；
5. 客户端仅在 **TLS 安全通道** 上发送明文密码；非 TLS 连接返回
   `ERROR 2061 (HY000): authentication requires a secure (TLS) connection`。

`--default-auth` 场景下，插件首次被调用时尚未拿到盐值（服务端握手插件与
`--default-auth` 不一致），此时 `read_packet()` 会触发空握手响应并读到
AuthSwitchRequest，插件返回 `CR_OK_HANDSHAKE_COMPLETE`，由客户端核心重新
处理切换并以缓存盐值再次调用插件完成认证。

## Docker / Linux 环境

官方 `mysql:5.7` 等镜像中的客户端**静态链接** libmysqlclient，且不导出
`mysql_get_ssl_cipher` 等符号，因此本机（macOS）编译的 `.so` 无法在容器中加载
（报 `invalid ELF header` 或 `undefined symbol`）。请使用 Linux 版产物：

```bash
./build.sh linux                    # 本机为 x86_64 → build/linux/x86_64/5.7/
./build.sh linux --arch aarch64     # ARM64 → build/linux/aarch64/5.7/
docker cp build/linux/x86_64/5.7/tidb_sm3_password.so <容器>:/usr/lib64/mysql/plugin/
docker exec -it <容器> mysql -h host.docker.internal -P 4000 -u user03 \
    --default-auth=tidb_sm3_password -p
```

或直接运行 `sh test/docker_test.sh` 在 mysql:5.7 容器内完成四项连接测试
（ARM 主机上先执行 `./build.sh linux --arch aarch64`）。

其他容器版本选择对应的构建目录即可（如 `mysql:8.0` 正式版 → `8.0.27+/`；
旧版 `mysql:8.0.0` 开发版 → `8.0.0-8.0.10/`）。

### 架构（CPU 平台）选择

插件的 `.so` 必须与加载它的 mysql 客户端**同架构**（Mach-O/ELF 的 CPU 类型不匹配
会直接加载失败）。结构体偏移已在 x86_64 与 arm64（aarch64）上逐版本验证一致，
源码无需按架构修改，只需按目标架构编译：

| 运行环境 | 客户端架构 | 使用产物 | 构建方式 |
|---|---|---|---|
| Intel Mac (x86_64) | x86_64 | `build/macos/x86_64/<版本>/` | `make`（本机） |
| Apple Silicon Mac (arm64) | arm64 | `build/macos/aarch64/<版本>/` | ARM 机上 `./build.sh`，或在本机 `./build.sh macos --arch aarch64` |
| Linux / Docker x86_64 | x86_64 (amd64) | `build/linux/x86_64/<版本>/` | `./build.sh linux` |
| Linux / Docker ARM64 | aarch64 | `build/linux/aarch64/<版本>/` | `./build.sh linux --arch aarch64` |
| 其他 Linux 架构 (arm/ppc64le/...) | 同左 | 同左 | `./build.sh linux --arch <架构>` |

> 补充：Apple Silicon Mac 若运行的是 Rosetta 2 转译的 x86_64 客户端，则使用
> x86_64 产物也可以；但标准安装（官方安装包 / Homebrew）均为 arm64 客户端，
> 请使用 arm64 产物。x86_64 与 arm64 的产物不可混用。

### TLS 检测的两种机制

插件不依赖链接时的符号解析（否则静态链接客户端 dlopen 即失败），而是在运行时：

1. 通过 `dlsym(RTLD_DEFAULT, "mysql_get_ssl_cipher")` 解析官方 API —— 适用于
   动态链接 libmysqlclient 的客户端（macOS 安装包、多数发行版）；
2. 解析不到时（静态链接客户端），回退为直接读取 `mysql->net.vio->type`
   （`MYSQL.net` 与 `NET.vio` 在各版本均为偏移 0；`type` 成员偏移经官方头文件
   验证：5.7 为 288，8.0/9.x 为 20），并对取值做范围校验，异常时 fail-closed
   （视为非安全通道）。

## Windows 环境

MySQL 在 Windows 上的客户端 ABI 与 macOS/Linux 不同（例如 `MYSQL.passwd`
偏移为 680 而非 704/688），因此必须使用独立的 Windows 构建：

```bash
./build.sh windows                # → build/windows/x86_64/{5.7, 8.0.0-8.0.10, 8.0.11-8.0.26, 8.0.27+}/
```

产物为 PE DLL（附 `.pdb` 调试符号），只导出 `_mysql_client_plugin_declaration_`，
依赖仅系统 UCRT/KERNEL32，无 libmysqlclient 依赖。安装方式：

```bat
copy build\windows\x86_64\5.7\tidb_sm3_password.dll ^
     "C:\Program Files\MySQL\MySQL Server 5.7\lib\plugin\"
mysql -h 127.0.0.1 -P 4000 -u user03 --default-auth=tidb_sm3_password -p
```

或使用 `--plugin-dir=<目录>` 指定插件目录。Windows 客户端无 dlsym，插件直接
使用 `mysql->net.vio->type` 检测 TLS（偏移已按 Windows ABI 验证一致）。
ARM64 Windows 客户端可用 `./build.sh windows --arch aarch64`（实验性）。

## 源码编译指南（自动适配架构）

`make` 会自动检测构建环境的操作系统与 CPU 架构，产出到对应目录，无需手动
指定：

| 构建环境 | 执行命令 | 产物位置 |
|---|---|---|
| macOS Intel | `./build.sh` | `build/macos/x86_64/<版本>/` |
| macOS Apple Silicon | `./build.sh` | `build/macos/aarch64/<版本>/` |
| Linux x86_64 | `./build.sh` | `build/linux/x86_64/<版本>/` |
| Linux arm64 | `./build.sh` | `build/linux/aarch64/<版本>/` |
| 任意主机 → 其他平台 | `./build.sh <os> [--arch <arch>]` | 对应目录 |

自动适配规则：`uname -s` 识别平台（Darwin→macos，Linux→linux），`uname -m`
识别架构（arm64 统一归一化为 aarch64 目录名）。所有构建共用同一份源码与
vendored 头文件；`MYSQL_VERSION_ID` 决定客户端插件接口版本（0x0100/0x0101/
0x0200），编译目标决定平台 ABI 布局，两者均无需人工干预。

## 安全说明

- 明文密码仅在 TLS 通道上传输（与服务端自动 TLS / 显式配置 TLS 配合）；
- 该服务端实现不提供 RSA 公钥交换，因此非 TLS 连接无法完成 full-auth，
  插件会明确报错而不是降级为明文；
- 服务端 `mysql.user.authentication_string` 存储 SM3 crypt 哈希
  （`$A$005$...`，与 caching_sha2_password 同格式，仅哈希算法不同）。

## 测试

```bash
make test     # 离线：SM3 标准向量、流式边界、真实交换已知答案、
              #       插件描述符 ABI、各 ABI 认证流程（mock VIO）
make connect  # 真实：对运行中的服务端执行 4 项连接测试
```

`make connect` 默认连接 `127.0.0.1:4000`、用户 `user03`、密码 `TiDB@123`，
可用环境变量 `HOST/PORT/DB_USER/DB_PASS/MYSQL/PLUGIN_DIR` 覆盖。测试项：

1. `--default-auth` + TLS → 认证成功；
2. `--default-auth` + `--ssl-mode=DISABLED` → 拒绝明文（ERROR 2061）；
3. 不指定 `--default-auth`（AuthSwitch 按名匹配）+ TLS → 认证成功；
4. 错误密码 + TLS → 服务端拒绝（ERROR 1045）。

## License

GPL-2.0（与 MySQL 客户端插件一致）。SM3 实现参考 GB/T 32905-2016 规范，
无外部加密库依赖。
