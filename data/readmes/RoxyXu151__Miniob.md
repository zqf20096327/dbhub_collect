# Miniob

**简体中文** | [English](README.en.md)

MiniOB 数据库内核学习与比赛代码，基于 OceanBase 社区项目，包含 SQL 解析、执行、存储、索引与事务等模块。保留原项目文档、贡献者和版权说明。

## 环境要求

按 docs/docs/how_to_build.md 准备 Linux / 容器开发环境、C++ 工具链、CMake 及第三方依赖。Windows 可采用文档中的容器开发方式。

## 获取仓库

```bash
git clone https://github.com/RoxyXu151/Miniob.git
cd Miniob
```

私有仓库需要先通过 GitHub 认证。以下相对路径与操作均以本仓库为起点。

## 安装与启动

```bash
git submodule update --init --recursive
bash build.sh --make -j4
```

## 配置与准备

配置文件为 etc/observer.ini。构建目录可能为 build_debug 或 build_release，以脚本输出为准；不要混淆开发容器的 SSH 端口与数据库服务端口。

## 使用方法与产物

进入实际构建目录后运行 ./bin/observer -f ../etc/observer.ini -P cli 可直接输入 SQL；TCP 模式可用 -p 6789 启动并通过同目录的 obclient 连接。更多模式见运行文档。

## 仓库导览

- [src](src)
- [unittest](unittest)
- [benchmark](benchmark)
- [etc](etc)
- [docs/docs/how_to_build.md](docs/docs/how_to_build.md)
- [docs/docs/how_to_run.md](docs/docs/how_to_run.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
- [NOTICE](NOTICE)
- [docker/README.md](docker/README.md)
- [原有详细资料](README.reference.md)：保留历史设计、截图和说明；涉及启动配置时以上述核对说明为准。

## 验证与常见问题

先执行小规模建表、插入与查询，再按 unittest/ 和比赛文档运行对应测试。并发和事务能力取决于构建选项与实现，不将教学数据库作为生产数据库使用。

## 维护与贡献

修改功能或使用方式时同步更新中英文 README。问题反馈请附复现步骤、环境版本与去除敏感信息后的日志；提交改动时说明实际完成的验证。

## 许可与来源

许可条款以仓库的 [License](License) 为准。第三方代码、数据、模型、论文与素材保留各自的许可和署名。
