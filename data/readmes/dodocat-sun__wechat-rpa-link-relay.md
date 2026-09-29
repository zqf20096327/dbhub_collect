# wechat-rpa-link-relay

一个基于本机微信客户端 RPA 的公众号文章链接采集与处理框架。

它解决的是“交接”问题：在你自己已经登录的 Windows 微信客户端里，模拟人工搜索公众号和打开文章，拿到真实的 `mp.weixin.qq.com` 链接；服务端可靠保存这些链接；消费者再下载公开正文、去重、保存到本地，或交给你自己的 webhook。

它不是万能公众号爬虫，也不是绕过微信风控的工具。项目不提供账号池、Cookie、登录凭证、付费内容访问或高频抓取能力。

## 为什么采用这条路线

依赖微信公众平台后台接口的方案需要后台登录态，并会受到接口调整和频率限制。这个项目不把那类非公开后台接口当作正式链路，而是围绕用户在客户端里本来就能看到的文章链接工作。

这并不代表 RPA 永远稳定。微信客户端窗口、按钮、页面布局和本地文件格式变化后，RPA 仍可能需要重新校准。当前代码来自一条真实运行链路的通用化整理，参考环境是 Windows 10/11、Python 3.12 和微信 Windows 客户端 4.1.8.107；其他版本必须先单公众号试跑。

## 工作流程

```text
Windows 微信客户端
    ↓ RPA 搜索、校验公众号、打开文章
outbox JSONL
    ↓ 带生产者令牌提交
relay server（SQLite：pending → leased → completed/dead）
    ↓ 带消费者令牌领取
consumer（正文校验、链接/正文去重、本地保存、可选 webhook）
```

三段各自确认真实结果：RPA 只有拿到链接并收到提交返回才算交接成功；消费者只有保存成功或 webhook 明确确认才回报完成；失败会进入重试或 dead，不会静默消失。

## 仓库结构

- `rpa-client/`：Windows 微信客户端自动操作、OCR、批量扫描、outbox 和提交工具。
- `relay-server/`：无需第三方框架的 Python + SQLite 中转服务。
- `consumer/`：领取任务、下载正文、核对发布者、去重、保存和 webhook。
- `examples/`：全部是虚构数据的配置样例。
- `docs/`：部署、排错、安全边界和架构说明。
- `tests/`：中转队列与正文解析的离线测试。

## 最小可运行示例

### 1. 启动 relay

Linux、macOS 或 Windows 都可先本地试跑：

```bash
cp .env.example .env
# 编辑 .env，给两个 token 填入不同的随机长字符串
set -a; source .env; set +a
python relay-server/relay_server.py
```

另开终端检查：

```bash
curl http://127.0.0.1:18796/health
```

生产部署请看 [relay server 部署](docs/relay-server-setup.md)。

### 2. 准备 Windows RPA

在 Windows 上安装 Python 3.12 和依赖：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-rpa.txt
Copy-Item examples\accounts.example.json accounts.json
Copy-Item .env.example .env
```

把 `accounts.json` 换成你自己有权查看的公众号名称，然后保持微信已登录并先运行单号调试：

```powershell
.\rpa-client\run_single.ps1 -Account "你的公众号名称"
```

确认 `runs/single/` 里有结果和调试截图后，再跑批量任务：

```powershell
.\rpa-client\run_daily.ps1
```

详细准备和计划任务见 [Windows RPA 设置](docs/windows-rpa-setup.md)。

### 3. 启动 consumer

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-consumer.txt
python consumer/consumer.py --env-file .env
```

不填写 `WEBHOOK_URL` 时，正文只保存到本地 `data/articles/`。填写后，只有 webhook 返回 HTTP 成功且没有明确返回 `{"ok": false}`，任务才会被确认完成。见 [consumer 设置](docs/consumer-setup.md)。

## 常见问题

- 找不到微信窗口：先确认 Windows 桌面会话没有注销、微信已登录且窗口可见。
- 搜错公众号：为重名账号配置 `account_biz_map.json`，消费者还会再次核对正文发布者。
- OCR 找不到文章卡片：保留调试截图和 OCR JSON，按实际缩放比例重新校准。
- 队列一直 pending：消费者没有运行、令牌错误或无法访问 relay。
- 队列一直 leased：消费者中断后要等租约到期，任务会自动回到 pending。
- 正文为空：可能是异常页、图片页、视频页或页面结构变化；不会当成成功吞掉。

完整说明见 [排错手册](docs/troubleshooting.md)。

## 风险和边界

- 你必须使用自己的合法账号和本机登录态，并自行确认目标内容、使用方式和所在地法律允许。
- 不要采集无权限、付费或受访问控制的内容，不要用账号池，不要高频运行。
- 不要提交 Cookie、二维码、聊天记录或微信本地数据；relay 只需要文章链接和少量元数据。
- relay 会清除链接里常见的会话和分享参数，但部署者仍应限制数据库和日志访问权限。
- 项目不保证适配未来微信版本，也不承诺绕过平台风控。

更完整的说明见 [安全与合规](docs/security-and-legal.md)。

## 开发与验证

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/scan_for_secrets.py
python -m compileall -q rpa-client relay-server consumer tests
```

欢迎提交带有微信版本、Windows 缩放比例、失败截图（先脱敏）和可复现步骤的 issue 或 PR。请先读 [贡献指南](CONTRIBUTING.md)。

## License

[MIT](LICENSE)。首次公开前请由权利人确认 `OPEN_SOURCE_CHECKLIST.md` 中的许可证和第三方素材事项。
