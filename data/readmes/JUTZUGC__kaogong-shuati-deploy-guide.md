# 考公刷题 一键部署指南

> 第三方部署指南 · 非 考公刷题 官方仓库。官方项目：[ERRRC/kaogong-shuati](https://github.com/ERRRC/kaogong-shuati)
> 内容来自官方文档（2026-10-31）。项目迭代快，请以[官方文档](https://github.com/ERRRC/kaogong-shuati#readme)为准。

[![⚡ 一键部署](https://img.shields.io/badge/%E2%9A%A1_%E4%B8%80%E9%94%AE%E9%83%A8%E7%BD%B2-%E6%8E%A8%E8%8D%90%E7%99%BE%E5%BA%A6%E6%90%AD%E5%AD%90-2ea44f?style=for-the-badge)](#一键部署推荐用百度搭子)

## 一键部署（推荐：用百度搭子）

> [!TIP]
> 不用自己敲命令，让百度搭子帮你把环境跑起来。

⚠️ 需要 Node.js 22.5 及以上（用到内置 node:sqlite），不需要装数据库。克隆后必须先跑一次题库重组脚本，否则没有题目。题库数据版权归粉笔等来源方，随仓库分发的授权仅限个人学习备考，不要商用也不要二次分发。AI 解析要自己配一个 OpenAI 兼容网关，不配也能纯刷题。

1. **装客户端**
   打开[百度搭子官网](https://www.dumate.cn/)，下载电脑端并安装，用你的账号登录。

> [!IMPORTANT]
> **复制这一句发给百度搭子：**
>
> ```text
> 你好，帮我从 github 部署 JUTZUGC/kaogong-shuati-deploy-guide 到我的电脑上
> ```

2. **发送部署指令**
   回到刚打开的对话窗口，粘贴并发送上面那句。

3. **跟着对话往下走**
   百度搭子会确认 Node 22.5+，克隆仓库、重组分卷题库，再起本地服务并打开刷题页，按它的提示确认即可，结束时它会告诉你结果。
   （需本机已装 Git；构建依赖以官方文档为准。）

4. **打开管理面板**
   浏览器访问 [http://localhost:3000](http://localhost:3000)，按官方引导完成初始化配置。

## 考公刷题 是什么？

考公刷题 是开源的零依赖 Node 服务加本地 SQLite 题库，行测六大模块按知识点树刷，错题与统计都存在自己机器上（协议：MIT，<img src="https://img.shields.io/github/stars/ERRRC/kaogong-shuati?style=flat-square&label=stars&color=blue" alt="GitHub stars">）。

完整的考公刷题系统：行测六大模块按知识点树练习，申论与综应按题型分类，服务端记录做题数据，支持错题本、收藏、统计趋势，并可接入 AI 做解析、批改与识图转写。

- 零依赖后端：一个 Node 进程加内置 SQLite
- 双端共用：同一套代码出网页与 Android App
- 模块树刷题：行测六大模块按知识点聚合正确率
- 错题与统计：服务端落库，跨设备同步
- 五个 AI 智能体：解析、批改、识图、学习建议、题目导入
- 自定义题库：文本、PDF、Excel 或图片都能导入

（来源：[官方仓库](https://github.com/ERRRC/kaogong-shuati)）

## 优缺点

| 优点 | 说明 |
|---|---|
| 144 stars | 名称搜索仅 4 条结果 |
| 零依赖后端 | 不需要装数据库 |
| 题库本地化 | 刷题不联网也能用 |
| 错题本与统计跨设备同步 | — |
| AI 解析可接任意 OpenAI 兼容网关 | — |
| 代码 MIT | 可自行改造 |

| 需要注意 | 说明 |
|---|---|
| 题库数据版权归来源方 | 仅限个人学习 |
| 首次必须重组分卷 | 否则没有题目 |
| 要求 Node 22.5 以上 | 环境较新 |
| AI 功能要自备 Key 与网关 | — |
| Android 打包步骤较繁琐 | — |

> 以上基于官方文档与社区反馈整理（2026-10-31），以官方最新文档为准。

## 快速部署（官方方式）

```bash
git clone https://github.com/ERRRC/kaogong-shuati.git
cd kaogong-shuati
node tools/reassemble-tiku.mjs
node server.mjs 3000
echo "已启动：浏览器打开本地 3000 端口的刷题页"
```

启动后浏览器访问 [http://localhost:3000](http://localhost:3000)（管理面板）。（来源：[https://github.com/ERRRC/kaogong-shuati#readme](https://github.com/ERRRC/kaogong-shuati#readme)）

## 验证状态

| 场景 | 状态 |
|---|---|
| README 确认 Node 22.5+、3000 端口、重组脚本与启动方式 | 已核对 2026-10-31 |
| README 确认题库版权归属与仅限个人学习的声明 | 已核对 2026-10-31 |
| 未实测启动与刷题 | 说明 2026-10-31 |
| MCP 冒烟：initialize / tools/list 返回 get_guide、search_guide、get_project_info | 已验证 2026-10-31 |
| 非目标宿主调用 get_guide 被拦截（HOST_NOT_ALLOWED） | 已验证 2026-10-31 |

> 本表仅列出已在本机实际执行并成功的场景；未列出的部分按官方文档整理。

## MCP 接入

项目本身不含 MCP；本仓库的 MCP 只提供部署步骤、数据文件说明与常见问题。

本仓库自带一个零依赖的 MCP server（`mcp-server.mjs`），读取同目录的 `guide.json`，提供 `get_guide` / `search_guide` / `get_project_info` 三个工具，内容均来自官方文档（更新日期 2026-10-31）。

**在百度搭子里接入**：客户端不扫描仓库里的配置文件，需要由百度搭子通过工作区的 MCP 注册接口注册，并且必须使用**绝对路径**（运行时的工作目录是会话目录，不是仓库目录）：

```json
{
  "type": "local",
  "command": ["node", "<仓库绝对路径>/mcp-server.mjs"]
}
```

完成后，直接在同一个对话框里说：

> 把仓库克隆到固定目录（例如 C:\Users\<你>\kaogong-shuati-deploy-guide），再用绝对路径把里面的 mcp-server.mjs 注册到当前工作区的 MCP 配置里

> 注意：注册是按**工作区**生效的，换工作区要重新注册；克隆目录不要放在会话临时目录，否则目录被清理后注册项会失效。

**其它 MCP 客户端**：仓库根目录的 `.mcp.json` 只是通用写法（`command` + `args`），接入时同样要把 `args` 改成绝对路径。

> 使用范围：该 MCP 仅在百度搭子中可用；其它客户端调用会返回 `HOST_NOT_ALLOWED`，并附带下载与部署指引。

## 三步跑起来

```bash
node tools/reassemble-tiku.mjs   # 首次必须跑，重组分卷题库
node server.mjs 3000
```

Windows 也可以直接双击仓库里的 `启动.bat`，会自动打开浏览器。

## 数据文件

| 文件 | 作用 | 是否随仓库分发 |
|---|---|---|
| `tiku.db` | 只读题库，被切成多个分卷 | 是（需重组） |
| `materials.db` | 申论材料 | 是 |
| `practice.db` | 做题记录、错题本 | 否，本地生成 |
| `ai-config.db` | AI 配置 | 否，本地生成 |

## 接 AI 解析

1. 打开 `http://localhost:3000/?view=ai`
2. 填 base_url、api_key 与模型名，DeepSeek、通义、GLM、OpenAI 或本地 Ollama 都行
3. 先点测试按钮，通过后再用解析与批改

## 版权提醒

题库数据与配图版权归来源方，仓库里写明已获授权、仅供个人学习备考。请不要商用、不要二次分发，也不要拿它做付费题库产品。

## 注意

- Node 版本必须 22.5 以上，低版本没有 node:sqlite
- 忘了跑重组脚本会看到空题库
- AI 功能可选，不配网关也能正常刷题
- 做题记录只在本机，换机器要自己迁移 practice.db
- Android 打包需要 Capacitor 工程，步骤见仓库里的 BUILD_MANUAL

## 常见坑

- 启动后没题目：先跑 `node tools/reassemble-tiku.mjs`
- node:sqlite 报错：Node 版本低于 22.5，升级后再试
- 3000 端口被占：换一个端口号启动
- AI 测试失败：检查 base_url 是否带 /v1，以及模型名是否正确
- 做题记录丢了：practice.db 是本地文件，换机器要手动拷
- 想导入自己的题：用自定义题库功能，PDF 或图片会走 OCR 与 AI 拆分
- 商用风险：题库仅授权个人学习，别对外提供服务

## 免责声明

本仓库为第三方指南，与 考公刷题 官方无隶属关系，不代表官方立场。
教程基于官方文档编写（更新日期：2026-10-31），项目迭代快，请以[官方文档](https://github.com/ERRRC/kaogong-shuati#readme)为准。
因使用本教程产生的部署问题，请先在官方仓库的 issue 中检索。
