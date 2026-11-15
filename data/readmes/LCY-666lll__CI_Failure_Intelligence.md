# CI Failure Intelligence

[![Backend CI](https://github.com/LCY-666lll/CI_Failure_Intelligence/actions/workflows/backend-ci.yml/badge.svg)](https://github.com/LCY-666lll/CI_Failure_Intelligence/actions/workflows/backend-ci.yml)

**从一次 CI 失败，找到可追溯的诊断线索。**

接收 GitHub Actions 的 JUnit 报告，将失败证据、同仓库相似历史和 AI 诊断放在同一个工作台。诊断中的引用可直接跳转到原始失败，方便核对上下文。

**[打开工作台](https://cifailure.xyz)** · [接入与使用](#接入与使用) · [GitHub Actions 接入说明](docs/GITHUB_ACTIONS_INTEGRATION.md)

![CFI 工作台：失败证据、相似历史与 AI 诊断](docs/images/workspace.jpg)

## 在工作台里完成失败调查

- **查看失败证据**：测试名称、错误信息、堆栈与 CI 运行身份集中展示。
- **对照相似历史**：检索同仓库的历史失败，点击来源事件核对原始记录。
- **阅读结构化诊断**：结论摘要、可能原因、建议操作与待补充信息，均保留证据上下文。
- **按需生成，复用结果**：已有有效诊断直接复用；读取结果不会触发模型调用。

## 接入与使用

**只看已有记录，完成第 1、2 步即可。接入自己的仓库，继续第 3～5 步；需要 AI 诊断时再做第 6 步。**

### 1. 领取访问凭据

通过 [GitHub Issues 申请访问](https://github.com/LCY-666lll/CI_Failure_Intelligence/issues/new?title=%E7%94%B3%E8%AF%B7%E8%AE%BF%E9%97%AE%20CFI)，说明你要查看记录、接入仓库，还是生成诊断。维护者确认后通过约定的私下渠道发放凭据；请勿在公开 Issue 中粘贴令牌、密钥或私有报告。

| 凭据 | 用途 | 填写位置 |
|---|---|---|
| 读取令牌 | 查看记录与已有诊断 | 网页入口 |
| CI 接入 HMAC 密钥 | 让 GitHub Actions 投递报告 | 目标仓库的 Actions Secret |
| 诊断触发令牌 | 授权生成 AI 诊断 | 事件详情的诊断区域 |

三者不能混用，也不是 GitHub Personal Access Token。使用线上服务无需安装本项目或提供自己的模型 API Key。当前采用共享工作区，受邀读取者可查看其中已接入的仓库记录。

### 2. 打开网页，进入工作台

打开 **[cifailure.xyz](https://cifailure.xyz)**，粘贴**读取令牌**，点击“**进入工作台**”。令牌保留在当前标签页，刷新可继续使用；点击“断开”可清除。

<details>
<summary>查看网页访问入口</summary>

![粘贴读取令牌并进入工作台](docs/images/access.jpg)

</details>

### 3. 在你的 GitHub 仓库填两项配置

进入**要发送报告的仓库**，打开 **Settings → Secrets and variables → Actions**：

| 在哪里新建 | Name | 填入的值 |
|---|---|---|
| **Variables → New repository variable** | `CFI_INGEST_URL` | `https://cifailure.xyz/api/v1/ci-runs/ingest` |
| **Secrets → New repository secret** | `CFI_INGEST_HMAC_SECRET` | 维护者发放的 **CI 接入 HMAC 密钥** |

分别点击 **Add variable / Add secret** 保存。网页读取令牌和诊断触发令牌不用填到 GitHub。

<details>
<summary>查看两项配置的填写示例</summary>

**接入地址填在 Variables。**

![GitHub 接入地址变量填写示例](docs/images/github-variable.jpg)

**HMAC 密钥填在 Secrets。图中用说明文字代替真实密钥。**

![GitHub HMAC 密钥填写位置，不展示真实密钥](docs/images/github-secret.jpg)

</details>

### 4. 给测试 workflow 接上发送步骤

两项配置保存后，还需要让 CI **在测试失败时发送 JUnit XML**：

1. 将[发送脚本](scripts/ci/send_ci_failure.py)放入你的仓库，保持路径为 `scripts/ci/send_ci_failure.py`。
2. 按[接入说明](docs/GITHUB_ACTIONS_INTEGRATION.md)在测试 Job 后接上发送步骤，对齐**测试步骤 ID、JUnit 路径、Python 运行环境**。
3. 提交并运行 workflow；测试全部通过时不会投递失败报告。

运行 ID、提交、分支等信息由 workflow 自动传入，不需要再到 Settings 逐项配置。

<details>
<summary>查看本项目 workflow 中的发送步骤</summary>

![workflow 从 Variables 和 Secrets 取值并发送 JUnit 报告](docs/images/github-workflow.jpg)

</details>

### 5. 确认投递，在网页查看失败

在 GitHub **Actions → 对应运行 → 测试 Job** 中查看发送步骤。看到“**原始 CI 失败事件已保存**”即表示投递成功；测试 Job 本身仍会保留失败状态。

![真实 CI 演练中的投递成功回执](docs/images/ci-receipt.jpg)

回到工作台点击“**刷新列表**”，按仓库和运行 ID 找到事件。报告由后台自动解析；若仍在等待，稍后点击“**刷新详情**”（后台每轮完成后等待 5 分钟）。解析后即可查看失败明细与相似历史。

![失败明细与可回溯的同仓库相似历史](docs/images/failure-history.jpg)

### 6. 按需生成 AI 诊断

进入事件详情，在 **AI 诊断**区域点击“**使用授权令牌触发诊断**”，填写独立的**诊断触发令牌**，再点“**确认触发**”。

![AI 诊断触发入口及独立令牌输入框](docs/images/diagnosis-trigger.jpg)

生成完成后，页面展示结论、可能原因和建议；点击“**当前证据**”或“**历史事件**”可回到来源。命中缓存会提示复用，任务处理中会自动查询结果。新生成可能产生模型费用，报告接入和解析不会自动触发付费诊断。

<details>
<summary>查看一份完整的 AI 诊断结果</summary>

![真实保存的结构化诊断结果与当前、历史证据引用](docs/images/diagnosis-result.jpg)

</details>

以上工作台截图来自线上验收样例；诊断为实际已保存的结果。

## 常见问题

| 遇到的问题 | 先检查这里 |
|---|---|
| 网页提示令牌无效 | 使用维护者发放的读取令牌；不要填 HMAC 密钥或诊断触发令牌 |
| 配置了 GitHub，但网页没记录 | 测试是否失败并生成 JUnit，workflow 的发送步骤是否真正执行成功 |
| 投递返回 401 | HMAC 密钥是否与目标实例一致，请求时间是否正常 |
| 有失败明细，却没有诊断 | 诊断需由授权者单独确认生成；已有结果可直接阅读 |

## 技术与接口

Vue 3 / Vite · FastAPI · PostgreSQL · Redis · Qdrant / FastEmbed · LangGraph / LangChain / DeepSeek

PostgreSQL 保存业务事实，Qdrant 提供同仓库历史检索；LangGraph 编排证据读取、历史检索、缓存、模型调用及引用校验。

<details>
<summary>查看 HTTP 接口</summary>

根地址：`https://cifailure.xyz`

| 方法 | 路径 | 认证 |
|---|---|---|
| POST | `/api/v1/ci-runs/ingest` | HMAC + timestamp + nonce |
| GET | `/api/v1/ci-runs?limit=20` | 读取 Bearer 令牌 |
| GET | `/api/v1/ci-runs/{event_id}/failures` | 读取 Bearer 令牌 |
| GET | `/api/v1/ci-runs/{event_id}/history` | 读取 Bearer 令牌 |
| GET | `/api/v1/ci-runs/{event_id}/diagnosis` | 读取 Bearer 令牌 |
| POST | `/api/v1/ci-runs/{event_id}/diagnosis` | 诊断触发 Bearer 令牌 |
| GET | `/health/live` | 无 |

`event_id` 是平台事件主键，不是 GitHub 的 `run_id`。

</details>

## 仓库结构

```text
backend/        API、业务服务、存储适配、迁移与测试
frontend/       Vue 工作台、证据导航与前端测试
scripts/ci/     CI 失败报告发送端
docs/           接入说明与产品截图
.github/        GitHub Actions workflow
infra/redis/    Redis 运行配置
compose.yaml    基础设施与后端服务
Dockerfile      后端镜像
```
