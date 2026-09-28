# DM8 一键安装与 Node.js 连接测试

安装脚本：`install-dm8.sh`。面向 OpenCloudOS 9 x86_64、systemd、root 权限的全新服务器。连接测试工具支持 Windows、Linux、macOS，需要 Node.js 18 或以上及 pnpm。

## Node.js 连接测试

在本项目目录执行：

```bash
pnpm install
```

复制配置模板（Windows PowerShell）：

```powershell
Copy-Item .env.example .env
```

Linux / macOS：

```bash
cp .env.example .env
```

编辑 `.env`，填写真实连接地址、端口、用户名和密码。例如通过 Nginx 的 4000 端口连接时，填写 `DM_PORT=4000`。数据库直连则填写安装时设置的端口。环境中已经存在的同名变量优先于 `.env`。

```dotenv
DM_HOST=your-server-address
DM_PORT=4000
DM_USER=TDM_DB_ADMIN
DM_PASSWORD="replace-with-your-password"
DM_TIMEOUT_MS=30000
```

运行：

```bash
pnpm test
```

也可直接执行 `node test-connection.js`。输出目标地址、账号、登录耗时，以及如下检查表：

| 检查项 | 示例结果 |
| --- | --- |
| 登录、SQL 查询 | 成功 |
| 当前用户 / Schema | TDM_DB_ADMIN |
| 大小写不敏感 | 已确认，值为 0 |
| MySQL 兼容模式 | 已确认，值为 4 |
| 字符集 | UTF-8 |
| 'abc' = 'ABC' | 成立 |
| 许可到期日 | 实际查询日期（北京时间） |

工具仅执行 SELECT，不创建表、不导入或修改数据。普通业务账号可能无权查询系统参数或许可证视图；单项失败会继续检查其他项目，不应把权限不足误判为网络失败。退出码 0 表示查询完成（配置是否符合预期看表格），1 表示配置、连接或查询出错，2 表示整体超时。

`.env` 已被 Git 忽略，不要提交真实密码。此项目未包含现有服务器凭据。

## 文件

- `install-dm8.sh`：全新 Linux 服务器安装脚本。
- `test-connection.js`：Node.js 只读连接测试。
- `.env.example`：测试配置模板。
- `package.json`：驱动依赖及测试命令。

## 执行安装

将脚本上传到服务器，例如 `/root/install-dm8.sh`，执行：

```bash
bash /root/install-dm8.sh
```

运行过程中会提示输入数据库监听端口，例如输入 `15236`；直接回车使用默认值 `5236`：

```text
请输入数据库监听端口 [5236]：15236
```

端口范围为 1024～65534，排除 DmAPService 使用的 4236；输入不合法或所选端口已被占用时会提示重新输入。此设置用于全新安装，不用于修改已有实例端口。外网访问还需安全组和防火墙放行对应端口；如果使用 Nginx TCP 代理，其后端端口也需与此一致。

按提示分别设置 SYSDBA 和 SYSAUDITOR 密码并确认，之后自动完成安装。密码需为 16～32 位，包含大小写字母、数字和特殊字符；允许字符为字母、数字以及 `@_!#%+=.-`。密码不写入脚本或配置文件，但初始化和验证时会短暂出现在本机进程参数中。不要用 `bash -x` 调试密码流程。

## 固定配置

| 项目 | 值 |
| --- | --- |
| 安装包 | `https://download.dameng.com/eco/adapter/DM8/202607/dm8_20260710_x86_rh7_64.zip` |
| 安装用户 / 用户组 | dmdba / dinstall |
| 安装目录 / 数据目录 | /opt/dmdbms / /data/dm |
| 数据库 / 实例 | DAMENG / DMSERVER |
| 端口 | 运行时交互输入，回车默认 5236 |
| 字符集 / 大小写 | UTF-8 / 不敏感 |
| MySQL 兼容模式 | COMPATIBLE_MODE=4（部分 SQL 兼容，连接需达梦驱动） |
| MEMORY_POOL / MEMORY_TARGET | 200 / 400 MB |
| BUFFER / RECYCLE | 512 / 128 MB |
| HJ_BUF_SIZE / HAGR_BUF_SIZE | 16 / 16 MB |
| 页大小 / 日志文件大小 | 32 KB / 256 MB |
| 服务 | DmServiceDMSERVER，开机自启 |

内存配置适用于开发环境，不是总内存硬上限。预检查要求可用内存至少 2 GiB，相关路径所在文件系统至少有 8 GiB 空间；最终资源需求随业务增长。

脚本使用官方静默安装 XML，仅安装软件，再单独初始化实例；下载后测试 ZIP 完整性，并对比包内 ISO SHA256。随包校验不是独立签名验证。

## 保护与验证

- 已有非空安装目录、数据目录、数据库服务或 DmAPService 时拒绝执行，因此不能在前面已完成安装的服务器上重复运行。
- 所选数据库端口被占用时提示重输，4236 被占用时停止；安装失败保留现场，不自动清理数据库，不支持断点续装。
- 不修改 Nginx、防火墙、安全组，不创建合作方账号，不覆盖项目环境变量。
- 软件安装、初始化使用 dmdba；服务注册使用 root；通过 systemd drop-in 设置文件句柄限制。
- 启动后以 DIsql 验证大小写、字符集、兼容模式，并查询实际许可到期日期。开发版有试用期限，并非永久免授权。
- 安装介质保留在输出的 `/opt/dm8-install.*` 目录；退出时卸载本次挂载的 ISO。验证日志权限为 600。

查看状态：

```bash
systemctl status DmServiceDMSERVER --no-pager -l
journalctl -u DmServiceDMSERVER -n 100 --no-pager
```

该版本及初始化配置已在本次会话的服务器上手动验证；一键脚本需在全新 OpenCloudOS 主机上验证完整安装流程，不能把本地语法检查等同于实机安装成功。

官方参考：

- https://eco.dameng.com/document/dm/zh-cn/pm/dm8-appendix.html
- https://eco.dameng.com/document/dm/zh-cn/ops/installation-install
- https://eco.dameng.com/document/dm/zh-cn/start/mysql_dm
