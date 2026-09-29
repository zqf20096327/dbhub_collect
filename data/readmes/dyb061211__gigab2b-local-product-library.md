# 大建云仓-GIGAB2B 本地商品库助手

一个面向 Windows 与 macOS 的本地商品资料管理工具：通过 GIGAB2B 官方 API 同步已授权 Buyer 账号的收藏商品，在本机整理价格、库存、Seller 公开信息、仓库分布、素材文件与历史记录，并导出可继续加工的 XLSX。

> [!IMPORTANT]
> 本项目是独立开发的非官方工具，与 GigaCloud Technology 或 GIGAB2B 不存在隶属、授权或背书关系。请只处理你有权访问的数据，并遵守网站条款、账号权限和适用法律。本项目不识别、破解或绕过验证码及 Safe Checker；出现验证时必须由用户本人完成。

## 主要功能

- 使用官方 Open API 增量同步收藏清单、商品详情、价格和 Seller 可售库存。
- 本地 SQLite 商品库，支持标题、Item Code、Seller、价格、库存、日期、素材和仓库条件筛选。
- Edge 扩展保存准确 Item Code / Product ID / 商品链接，并同步“我的收藏”页面可见的 Warehouse Code 与库存区间。
- 收藏库存同步支持逐页检查点：遇到 Safe Checker 后，人工验证并再次点击扩展即可从最后完整页继续；即使网页回到第 1 页，也会自动定位。
- Seller Store Profile 公开信息补全：邮箱、电话、手机、WhatsApp、网站和微信二维码。
- 每个 Item Code 独立资料目录；支持主图、商品图、官方素材包、认证文件与安装说明。
- XLSX 导出可包含主图缩略图、图片描述、Seller 联系方式、二维码链接和仓库明细。
- Windows 与 macOS 一键安装/启动脚本，运行数据只保存在本机。

## 数据来源与边界

| 数据 | 来源 | 说明 |
|---|---|---|
| 收藏、商品详情、价格、总库存 | GIGAB2B 官方 Open API | 需要用户自己的 API 凭据 |
| Warehouse Code、库存区间 | 已登录账号可见的“我的收藏”页面 | 由用户主动点击 Edge 扩展读取 |
| 仓库国家、州/省、城市、地址 | 官方仓库地址 API | 无法匹配时保持“未知”，不会猜测 |
| Seller 联系方式和二维码 | Store Profile 明确公开的内容 | 遮罩值与平台页脚不会保存 |

程序不会保存 GIGAB2B 用户名、密码、验证码或浏览器 Cookie。API Secret 只从本机 .env 读取；.env、SQLite、日志、缓存、截图和用户输出均被 Git 忽略。

## 环境要求

- Windows 10/11 64 位，或受支持的 macOS
- Python 3.12 或更高版本（64 位）
- Microsoft Edge
- 使用官方同步功能时，需要有效的 GIGAB2B Open API Client ID 与 Client Secret

## 快速开始

### Windows

1. 从 [Releases](https://github.com/dyb061211/gigab2b-local-product-library/releases) 下载名称含 “Windows” 的 ZIP。
2. 完整解压 ZIP，进入 GIGAB2B_商品库 文件夹。
3. 双击 install.bat，等待显示安装完成。
4. 双击 start.bat。浏览器会打开 http://localhost:8501。
5. 详细步骤和常见问题见 [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)。

### macOS

1. 从 [Releases](https://github.com/dyb061211/gigab2b-local-product-library/releases) 下载名称含 “macOS” 的 ZIP。
2. 完整解压 ZIP，进入 GIGAB2B_商品库 文件夹。
3. 首次运行若被 macOS 拦截，请在 Finder 中右键 install_mac.command，选择“打开”并再次确认。
4. 双击 install_mac.command，安装完成后双击 start_mac.command。
5. 详细说明见 [MACOS_GUIDE.md](MACOS_GUIDE.md)。

首次安装需要联网下载 Python 依赖。安装完成后，日常启动无需重复安装。

## 配置官方 API

也可以先不配置 API 打开空商品库。需要同步时，在应用左侧点击“账号与 API 设置”，直接在本机填写凭据；不要把 Secret 发到聊天、Issue 或截图中。

如需使用环境文件，可复制 .env.example 为 .env：

```dotenv
GIGA_API_ACCOUNT_LABEL=我的账号
GIGA_API_BASE_URL=https://openapi.gigab2b.com
GIGA_API_CLIENT_ID=你的_Client_ID
GIGA_API_CLIENT_SECRET=你的_Client_Secret
```

曾经公开、截图或发送过的 Secret 应先在官方后台轮换。

## 安装 Edge 扩展

1. 在 Edge 地址栏输入 edge://extensions/。
2. 开启“开发人员模式”。
3. 点击“加载解压缩的扩展”。
4. 选择 edge_extension/gigab2b_favorite_helper 文件夹。
5. 确认扩展版本为 **0.9.13**，然后刷新已经打开的 GIGAB2B 页面。

扩展只与本机 127.0.0.1 服务配对，不读取或上传 Cookie、密码、API Secret 或验证码。详细操作见 [扩展说明](edge_extension/gigab2b_favorite_helper/README.md)。

## 推荐工作流

1. 启动本地商品库并配置官方 API。
2. 在 GIGAB2B 正常收藏商品，或用扩展在搜索结果页辅助收藏并保存准确商品身份。
3. 在“收藏同步与任务”中同步新收藏；新商品完成详情、价格、库存和必要资料后才进入正式商品库。
4. 如需 Warehouse Code，在“我的收藏”清空筛选后点击扩展同步库存分布。
5. 如遇 Safe Checker，人工验证后再次点击扩展，选择从断点继续。
6. 如需 Seller 公开联系方式，先在本地生成补全任务，再由扩展复用一个已经登录的普通 Edge 标签页处理。
7. 在商品库勾选商品，按需导出 XLSX。

## 本地目录

```text
data/       SQLite 与本地状态
logs/       运行日志
output/     按 Item Code 保存的商品资料
release/    本地构建的发布包
```

这些目录不会提交到 GitHub。删除店铺分组不会删除商品；删除项目目录前请先备份 data/ 与 output/。

## 开发与测试

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -c requirements-lock.txt
.venv/bin/python -m pytest -q
```

Windows 对应命令：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -c requirements-lock.txt
.\.venv\Scripts\python.exe -m pytest -q
```

构建两个干净源码安装包：

```bash
.venv/bin/python -m tools.build_release --output-dir release --version 0.9.13
```

构建器会排除 .env、数据库、日志、缓存、用户输出、私钥和已打包扩展，并生成 RELEASE_MANIFEST.json 与 SHA256SUMS.txt。

## 文档

- [Windows 使用说明](WINDOWS_GUIDE.md)
- [macOS 使用说明](MACOS_GUIDE.md)
- [商品库详细说明](PRODUCT_LIBRARY_GUIDE.md)
- [安全政策](SECURITY.md)
- [参与贡献](CONTRIBUTING.md)
- [版本记录](CHANGELOG.md)

## 许可

Copyright © 2026 dyb061211. All rights reserved.

本仓库公开不代表授予开源许可。你可以在 GitHub 上查看源码、提交 Issue、Star 或 Fork；除非获得版权所有者的明确许可，不得复制、修改、销售或重新分发本项目及其衍生版本。GitHub 平台条款依法赋予的权利不受本声明影响。
