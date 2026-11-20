# 闲书书

Flask + SQLite + Playwright 的闲鱼图书采购管理系统。一个仓库包含 Windows 本地与 Linux 服务器运行代码。

功能包括多店铺订单及退款同步、采购绑定、物流核验回填、选品上架、图片素材、热书榜、文案模板、客户和利润报表。采购提交及付款由人工完成。

## 先看这里

**可以在自己的 Windows 电脑上运行。首次安装依赖后，可先用演示数据体验；真实业务需要你自己的闲管家接口授权和孔夫子账号。源码不附带任何账号、客户资料或平台授权。**

| 你要做什么 | 阅读说明 |
| --- | --- |
| 在自己电脑安装、启动、配置账号 | [Windows 安装与启动](docs/windows-install.md) |
| 同步订单、采购、发货、选品与日常维护 | [使用说明](docs/user-guide.md) |
| 安装 Edge / Chrome 浏览器助手 | [浏览器扩展安装](docs/browser-extension.md) |
| 部署到自己的 Linux 服务器 | [服务器部署说明](docs/server-deploy.md) |
| 修改代码、了解模块职责 | [架构说明](ARCHITECTURE.md) |
| 与最初源码、现用网站有何区别 | [版本对照](docs/version-comparison.md) |
| 准备发给别人、查看已测范围 | [分发验收](docs/distribution-check.md) |

建议第一次使用者选择 Windows 本地版。安装独立扩展后，在常用 Chrome / Edge 从订单货源入口进入孔夫子核对填址，在图池入口使用收图功能；也可使用“填单”打开项目专用浏览器。扩展 ZIP 下载后先解压，通过浏览器“加载解压缩的扩展程序”安装，目前尚未上架扩展商店。

[下载独立扩展 1.1.0](https://github.com/wutuobang888/xianshushu/releases/download/address-helper-v1.1.0/xianshushu-address-helper-1.1.0.zip) · [安装教程](docs/browser-extension.md)

[下载整套源码 1.1.2](https://github.com/wutuobang888/xianshushu/releases/tag/server-verified-v1.1.2)：包含 Windows 本地与 Linux 服务器代码、独立扩展及中文说明。

## Windows 本地快速体验

先安装 64 位 Python（源码使用 Python 3.10+ 语法）和 Microsoft Edge。下载仓库 ZIP 并解压，在包含 app.py 的文件夹打开 PowerShell。以下命令使用虚拟环境内的 Python，无需激活脚本：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/local_launch.py demo
```

打开 http://127.0.0.1:5000/orders 。保留终端窗口；结束时按 Ctrl+C。演示目录里不要填入真实凭据：填入后部分操作会调用真实平台。正式使用请按完整安装文档切换到独立的 data/live 目录。

首次安装后可双击 `scripts/run_app.bat` 体验演示，双击 `scripts/run_live.bat` 使用正式数据目录。两个入口均使用项目 `.venv`，默认不开业务任务；正式任务需验收后明确启用。

如果 Edge 未安装或准备改用 Chromium，浏览器安装与选择方法见完整安装说明。代码、文档与外部平台页面仍可能随环境不同出现兼容问题；不要把演示页面正常等同于真实采购与发货已经验证。

## Linux 服务器

安装 requirements-server.txt 和 Playwright Chromium；参考 deploy/ 下的环境变量与 systemd 配置模板。模板中的 /srv/xianshushu 路径需要按实际部署修改。

正式 Web 使用 production_wsgi:app，必须设置 XIANSHUSHU_CLOUD_MODE=1、DEMO_MODE=0、XIANSHUSHU_SCHEDULER=0、FLASK_DEBUG=0，并配置独立随机 FLASK_SECRET_KEY、站内登录凭据文件与 HTTPS 反向代理。后台调度单独运行 worker.py，避免启动多个业务任务实例。浏览器交互另需显示服务及受认证保护的网关。

已在 GitHub 独立 QEMU Debian 13 / Python 3.13.5 虚拟机完成从零安装、HTTPS 登录、桌面网关、定时同步和整机重启自启验收。详见 [服务器验收记录](docs/server-verification.md)。真实平台账号需自行配置及核对；不要执行历史迁移脚本，仓库不提供这些脚本。

## 地址与采购限制

服务器同步默认地址成功后再进入普通孔夫子网页；提交前仍需人工核对收货人。共享账号、浏览器配送记忆与旧结算页快照可能影响选中结果。涉及地址簿轮换应由部署者明确启用，并保留备份及回读检查。

## 开源与验证

本仓库包含 Windows 本地和 Linux 服务器两种运行方式的源码。真实数据库、客户资料、登录态、密钥、日志和原 Git 历史均未收录。第三方前端资源保留其原文件中的许可证标注。项目代码采用 MIT 许可证，第三方资源见 THIRD_PARTY_NOTICES.md。

2026-11-15 安装验收：Windows / Python 3.10.11 全新虚拟环境，以及全新 Debian 13 / Python 3.13.5 服务器隔离系统均安装成功，pip check 通过。Windows 的演示/正式启动、数据持久化、扩展与实际本地网站集成通过；Linux 的 HTTPS、登录与 CSRF、浏览器桌面、worker 定时执行及重启通过。


独立扩展 1.1.0 统一提供采购填址、小红书/孔夫子收图和待付款提示回传，仓库当前版本不再分发脚本管理器安装文件。验证使用隔离浏览器及模拟订单，覆盖两位买家分别选址、两本书分别回到对应图池、来源会话及 CSRF 校验；未操作用户真实 Edge 账号，也未提交真实采购或付款。

回归检查：Linux 233 项 Python 测试逐模块隔离执行通过，18 项 JavaScript 测试通过。安装验收中的外部平台使用合成数据，不包含真实采购、付款或发货验证。详细范围见 [分发验收](docs/distribution-check.md) 和 [服务器验收](docs/server-verification.md)。
