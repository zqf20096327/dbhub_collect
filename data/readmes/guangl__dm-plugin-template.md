# dameng-cli 插件模板

点击本仓库的 **Use this template** 创建自己的插件仓库。模板包含可运行的 `hello`、进程级协议测试、跨平台 CI、六个平台的 GitHub Release 及 SHA-256；独立构建无需宿主源码目录。

## 改成自己的插件

1. 修改 Cargo.toml 的包名、binary 名、repository 和 description；例如 `dm-plugin-mytool`、`dm-mytool`。
2. 修改 dm-plugin.toml 的 name、description、homepage 与 min_host_version；name 必须对应 binary `dm-<name>`。Cargo.toml 与清单的 version 保持一致。
3. 修改 src/main.rs 的功能与 tests/protocol.rs 的预期；同步 scripts/build_release.sh、scripts/check_glibc.py、scripts/test_glibc_runtime.sh 中的 `dm-hello`，以及 Release workflow 的 artifact 名。
4. 修改 README、config.example.toml 和 LICENSE，提交 Cargo.lock。SDK 暂用固定 Git 提交，SDK 发布 crates.io 后可改成版本依赖。

## 验证

```sh
cargo fmt --all -- --check
cargo test --locked
cargo clippy --all-targets --locked -- -D warnings
RUSTDOCFLAGS="-D warnings" cargo doc --no-deps --locked
python3 scripts/test_release.py
```

## 本地安装

```sh
cargo build --release --locked
cp target/release/dm-hello ./dm-hello
dm install .
dm hello world
```

Windows 使用 `dm-hello.exe`。直接运行 binary 缺少宿主协议环境时应报错，正常入口是 `dm hello`。

## 独立发布

所有修改经功能分支、PR、CI 和维护者合并确认。同步 crate 与清单版本，确认后在合并提交创建对应的 `vX.Y.Z` 标签；Release workflow 验证版本并运行 CI，再发布九个平台安装包及 SHA-256（x86_64/ARM64 GNU 与 musl Linux、ARMv7 GNU Linux、Apple Silicon 与 Intel macOS、x86_64 与 ARM64 Windows）。GNU Linux 使用 glibc 2.28，musl 提供独立归档。Git 仓库安装所需的原始二进制及 SHA-256 也会发布。

正式 Release 发布后，用户可以使用 `dm install https://github.com/<owner>/<repository>.git --rev vX.Y.Z`，或下载、校验并解压安装包，再通过 `dm install <包目录> --release-source <owner>/<repository> --release-tag vX.Y.Z` 安装。

更多协议与分发约定见 [插件开发文档](https://guangl.github.io/dameng-cli/plugin-development/)。License: MIT。
