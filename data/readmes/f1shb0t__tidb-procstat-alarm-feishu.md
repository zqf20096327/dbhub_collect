# tidb-procstat-alarm-feishu

用 **CloudWatch Agent (procstat) → CloudWatch Alarm → SNS → Lambda → 飞书** 的链路，
监控自建 TiDB 集群中 **PD / TiKV / TiFlash** 三类组件的**进程存活**，进程挂掉即推送飞书告警卡片。

> 本方案只覆盖「组件进程死了要报警」这一层（+ 恢复通知）。
> 组件级健康（PD 选主 / TiKV write stall / TiFlash 同步延迟等）cwagent 采不到，
> 需另配脚本抓 `/metrics` 或保留 TiDB 原生 Prometheus+Alertmanager，见文末。

---

## 架构

```
EC2 (PD / TiKV / TiFlash，分别在不同实例)
   └─ CloudWatch Agent (procstat: pid_count)
          │  自定义 metric: namespace=TiDB/Procstat
          ▼
   CloudWatch Alarm  (pid_count < 1, treatMissingData=BREACHING)
          │
          ▼
   SNS Topic (tidb-procstat-alerts)
          │
          ▼
   Lambda (feishu_forwarder.py)  ── 转成飞书卡片 ──►  飞书群机器人 Webhook
```

**CDK 负责**：SNS Topic + Lambda + 订阅授权 + 每个「实例×组件」的 procstat Alarm。
**手动负责**：在各 EC2 上安装/配置 cwagent（本仓库 `cwagent/` 提供配置文件）。

---

## 一、部署 CloudWatch 侧（CDK）

### 1. 安装依赖
```bash
cd tidb-procstat-alarm-feishu
npm install
```

### 2. 配置
```bash
cp .env.example .env
# 编辑 .env：填 FEISHU_WEBHOOK_URL / FEISHU_WEBHOOK_SECRET
```

编辑 `bin/app.ts` 里的 `instances` 默认清单，改成客户真实实例 ID：
```ts
instances = [
  { instanceId: 'i-0aaa...', component: 'pd' },
  { instanceId: 'i-0bbb...', component: 'tikv' },
  { instanceId: 'i-0ccc...', component: 'tiflash' },
];
```
或部署时用 context 传入（免改代码）：
```bash
npx cdk deploy \
  -c instances='[{"instanceId":"i-0aaa","component":"pd"},{"instanceId":"i-0bbb","component":"tikv"}]' \
  -c feishuWebhookUrl='https://open.feishu.cn/open-apis/bot/v2/hook/xxx' \
  -c feishuWebhookSecret='xxx'
```

### 3. 部署
```bash
npm run build
npx cdk bootstrap        # 该账号/region 首次用 CDK 才需要
npx cdk deploy
```

---

## 二、部署 EC2 侧（CloudWatch Agent）

在**每台** PD / TiKV / TiFlash 实例上：

### 1. IAM
给 EC2 instance profile 挂 `CloudWatchAgentServerPolicy`。

### 2. 安装 Agent（Debian）
```bash
wget https://amazoncloudwatch-agent.s3.amazonaws.com/debian/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E ./amazon-cloudwatch-agent.deb
```

### 3. 放配置（按组件选对应文件）
```bash
# PD 节点
sudo cp cwagent/config-pd.json      /opt/aws/amazon-cloudwatch-agent/etc/config.json
# TiKV 节点
sudo cp cwagent/config-tikv.json    /opt/aws/amazon-cloudwatch-agent/etc/config.json
# TiFlash 节点
sudo cp cwagent/config-tiflash.json /opt/aws/amazon-cloudwatch-agent/etc/config.json
```
> 带全注释的总模板见 `cwagent/config-template.jsonc`，可读懂每一项后自行裁剪。

### 4. 启动 Agent
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/config.json -s
```

### 5. 验证 metric 上报
CloudWatch 控制台 → Metrics → 自定义命名空间 `TiDB/Procstat`，
应能看到 `procstat_lookup_pid_count`（维度含 `InstanceId`、`exe`）。

---

## 三、测试整条链路

1. **测试飞书转发**（不影响真实告警）：手动把某个 Alarm 置为 ALARM
```bash
aws cloudwatch set-alarm-state \
  --alarm-name TiDB-pd-down-i-0aaa \
  --state-value ALARM \
  --state-reason "manual test"
# 再置回 OK 验证恢复通知
aws cloudwatch set-alarm-state \
  --alarm-name TiDB-pd-down-i-0aaa \
  --state-value OK --state-reason "manual test recover"
```
2. **真实演练**：在某台 TiKV 上 `sudo systemctl stop tikv`（谨慎，非生产），
   1–2 分钟内应收到飞书红色告警卡片；恢复后收到绿色卡片。

---

## 关键坑位（务必知道）

- **`treatMissingData = BREACHING`**：进程死了 procstat metric 是**没有数据点**，
  不是变成 0。所以缺数据必须当作「触发告警」，否则进程死了反而不报警。CDK 已默认设好。
- **metric 名可能不同**：不同 cwagent 版本上报的可能是
  `procstat_lookup_pid_count`（默认）或 `procstat_pid_count`。
  若 Alarm 一直 `INSUFFICIENT_DATA`，去控制台看实际 metric 名，
  改 `lib/tidb-procstat-alarm-stack.ts` 里的 `metricName` 后重新 deploy。
- **`exe` 维度值**：必须与 cwagent procstat 的 `exe` 完全一致
  （`pd-server` / `tikv-server` / `tiflash`）。
- **namespace 一致**：cwagent 的 `metrics.namespace` 必须 = CDK `metricNamespace`。
- **飞书签名**：机器人 webhook 是公网可达，强烈建议开启签名校验并填 `FEISHU_WEBHOOK_SECRET`。
- **cwagent 用 `cwagent` 用户跑**：配置里已设 `run_as_user: cwagent`，
  别用 root 跑中间件相关进程（老经验）。

---

## 后续扩展（组件健康层，非本期范围）

procstat 只能判断「进程活/死」。若客户要「进程活着但不健康」的检测：
- 抓 PD `http://<pd>:2379/pd/api/v1/stores` + `/health` → 推自定义 metric → Alarm
  （一个接口即可覆盖三组件的「集群视角存活」，性价比最高）
- 或保留 TiDB 自带 Prometheus + Alertmanager，走同一个飞书机器人

需要时可在本项目基础上加一个「健康抓取脚本 + 自定义 metric Alarm」的模块。
