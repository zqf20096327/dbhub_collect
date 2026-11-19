# 提示词匣 · PromptCabinet

Windows 原生、离线优先的 AI 提示词收藏与复用工具。集中整理提示词、保留来源，并将不同模型生成的 HTML 作品与提示词一起归档和对比。

当前版本为 **0.1.0 预览版**，使用 WPF / .NET 10 和本地 SQLite。

## 当前功能

- **默认示例**：首次创建资料库时内置14条模型测试提示词（含黑洞），保留原文和分类，不附带HTML作品。既有空库或非空库不会自动补入，再次启动也不重复添加。
- **提示词资料库**：新建、阅读、编辑、复制、收藏、分类、标签、备注及回收站，支持本地搜索和中文 / English 界面。
- **模型作品归档**：关联模型及版本，导入单个 HTML / HTM 文件或根目录含 `index.html` 的静态目录，保存原始文件字节。每份作品最多 512 个文件、单文件 32 MiB、总量 128 MiB。
- **作品预览与对比**：使用 WebView2 主动打开单份作品，或并排对比 2–4 份作品。导入时默认允许指定 CDN 资源，可逐作品关闭。
- **公开来源搜索**：目前支持 prompts.chat 和 Prompt Motion。默认搜索先用用户自己的 DeepSeek Key 整理 1–3 个查询词，再查询来源站点；模型不生成搜索结果。缺少 Key 或规划失败时，可显式选择原词搜索。
- **搜索结果筛选**：普通搜索和原词搜索会保留已选来源与技术类型；共同来源保留选择，新增来源默认选中，移除来源不再显示。只有显式点击“全部 / 恢复筛选”才重新全选，筛选操作本身不联网。
- **结果保存**：保存前确认或手动修改标题，并选择已有分类或无分类。自动标题按当前界面语言转换；正文原文和来源原标题保留。
- **按需翻译**：完整网络正文可手动翻译并切回原文；译文仅在内存中展示，保存结果时仍保留原文。

## 从源码构建与运行

需要 Windows、**.NET 10 SDK** 和 **Microsoft Edge WebView2 Runtime**。作品预览还受本机 WebView2、GPU 与网络环境影响。

在仓库根目录的 PowerShell 中构建 Debug 版本；首次构建需要还原 NuGet 依赖：

```powershell
dotnet build '.\PromptCabinet.sln' -c Debug --artifacts-path '.\.artifacts\build' --nologo
```

构建成功后，正常关闭已打开的主窗口和预览窗口，再手动运行：

```powershell
& '.\.artifacts\build\bin\PromptCabinet.App\debug\PromptCabinet.App.exe'
```

启动会初始化本地数据库并执行适用迁移；已有资料请先备份。通过主窗口进入资料库，使用后正常关闭窗口即可退出。以上命令使用通用相对路径；本次检查使用独立产物目录，验证范围见下文。

## 数据、Key 与联网边界

应用数据根目录为 `%LocalAppData%\PromptCabinet\`：

| 位置 | 用途 |
| --- | --- |
| `Data\promptcabinet.db` | SQLite 资料库，保存提示词、分类、来源、模型信息及导入作品文件 |
| `settings.json` | 界面语言、布局及来源设置 |
| `PreviewSessions\` | 作品预览的临时会话数据 |
| Windows 凭据管理器中的 `PromptCabinet:DeepSeek` | 用户自己的 DeepSeek API Key；不写入数据库或明文设置文件 |

首次默认初始化失败时，整批示例回滚并上报错误，数据库文件保留；后续启动不会自动重播或补入示例。

本地资料的整理、阅读与复制不需要 DeepSeek Key。以下操作涉及外部网络：

- 默认搜索会将当前查询交给 DeepSeek 做查询规划，并向所选公开来源请求结果与正文；后续“更多”沿用已有计划。显式原词搜索不调用模型。
- 手动正文翻译会把所选正文发给 DeepSeek；准备网络结果的保存表单时，只把来源标题交给同一翻译客户端处理。没有 Key 或标题转换失败时，仍可手动填写标题。
- 作品开启指定 CDN 后，预览可向获准的 CDN 请求资源。关闭该选项会收紧资源访问，但不代表完整网络隔离。

DeepSeek 功能使用用户自己的账户和额度，使用前请了解对应服务的计费与隐私政策。请勿提交 Key、用户数据库或私人作品。

**作品预览面向用户信任的静态内容，不是恶意代码沙箱。** 不应将未知来源的 HTML 当作安全内容直接运行。

## 源码与设计

```text
src/
  PromptCabinet.App/             WPF 界面、应用装配、系统凭据与 WebView2 预览
  PromptCabinet.Application/     应用流程、设置、公开来源访问与模型客户端
  PromptCabinet.Domain/          保留的领域项目（当前尚无独立领域实现）
  PromptCabinet.Infrastructure/  SQLite 持久化、作品导入与预览缓存
tests/
  PromptCabinet.IntegrationTests/
docs/
  architecture/                 当前架构图及可编辑源
```

- [设计与数据模型](docs/设计与数据模型.md)
- [架构维护说明](docs/architecture/README.md)
- [当前架构图 HTML](docs/architecture/promptcabinet-current.html)（下载后可在浏览器打开）
- [可编辑架构图 JSON](docs/architecture/promptcabinet-current.json)
- [第三方资源告知](docs/architecture/THIRD_PARTY_NOTICES.md)

## 当前验证范围与已知限制

目录缓存改动已通过 Debug 构建 **0 警告、0 错误**，以及排除真实用户目录读取用例后的 **371/371 项集成测试**。其中包含默认示例的 **16 项 PromptLibraryTests**，覆盖首次新库、既有空库/非空库、重复启动和中途失败回滚。随后筛选选择保留改动再次通过 Debug 构建 **0 警告、0 错误**及 **95/95 项 MainWindowViewModelTests 聚焦检查**。两批结果分列、不相加，后一次未重跑整套；这些检查不代表 GUI、Release 或发布二进制通过。

- **Prompt Motion 首次或到期搜索仍可能较慢**：客户端在内存中复用成功解析的完整目录，成功解析后 5 分钟到期，命中不延长期限；每个新查询计划重新匹配与评估。有效期内可避免重复下载目录，首次、到期后及应用重启后的请求仍受外站网络影响；规划和其他来源请求仍有各自开销，不承诺固定提速。
- **部分右侧正文空白的报告仍待定位**：尚未复现并确认原因。
- 当前版本的 WPF 实际布局与交互、WebView2 / Three.js 作品效果，以及真实模型生成标题的质量尚未验证。
- 作品仅支持 HTML 文件或静态目录，不支持 ZIP 直接导入、npm 项目构建或多作品同步摄像机；不自动生成作品或评分。
- 网络来源适配目前限于上述两站，搜索结果的证据等级不代表全文质量验证或全网穷尽。

## 贡献与聚焦检查

反馈问题时请附复现步骤、Windows / WebView2 版本，以及必要的脱敏日志；涉及网页时保留公开来源链接。提交前排除用户数据、凭据和本地生成文件。

完成上面的 Debug 构建后，可运行以下安全范围集成检查。`RealDataDirectoryIsolationTests` 会读取真实用户目录，因此排除；当前测试源码不存在 `ApiKey_SaveThenClear`，过滤串保留该名称仅作历史凭据测试的防御项。

```powershell
dotnet test '.\tests\PromptCabinet.IntegrationTests\PromptCabinet.IntegrationTests.csproj' -c Debug --no-build --artifacts-path '.\.artifacts\build' --filter 'FullyQualifiedName!~ApiKey_SaveThenClear&FullyQualifiedName!~RealDataDirectoryIsolationTests' --nologo
```

仓库许可证尚未指定。
