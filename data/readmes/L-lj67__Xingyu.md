<p align="center">
  <img src="src/Xingyu.App/Assets/Xingyu.svg" width="72" alt="行域图标">
</p>

<h1 align="center">行域 Xingyu</h1>

<p align="center">一款以项目工作空间姿态驻留桌面的便笺。</p>

> 当前版本：v0.7.4 · Windows 10/11 x64 · 本地优先 · 无需账号

## 行域是什么

行域首先是一款便笺。它面向个人复杂事项，以一个持续存在的项目工作空间姿态驻留在 Windows 桌面。

它只有两个核心层级：上方是你的项目清单，下方是当前项目的自由工作区。项目状态、优先级、进度和提醒都是可选属性；用户不需要把自己的思考压缩成预设表格，也不需要先学会 Markdown。

```text
项目清单层
    ↓
项目工作空间层
```

它适合承载课程设计、论文、工程实践、长期学习以及任何需要反复返回并继续推进的个人项目。

## 主要功能

- 自由富文本书写：加粗、斜体、下划线、删除线、标题、列表、颜色与高亮
- 可调默认文字、标题字号和行距
- 图片粘贴与拖入，并随窗口自适应；单击后可继续缩小
- 文件附件卡片，可用系统默认程序打开
- 项目搜索、长按拖动排序、批量删除
- 可选状态、优先级、手动进度和多个本机提醒
- 项目卡可按进度或优先级自动着色
- 自由窗口、桌面固定组件和微型组件
- 可选置顶、背景透明度、布局记忆与快速呼出
- 默认快捷键为 `Ctrl + \`，可以修改或关闭
- 可选静默开机自启动
- 数据仅保存在本机，不要求登录

## 下载

普通使用者无需下载源代码。请在本仓库右侧的 **Releases** 中打开最新版本，并下载：

[下载 Xingyu-0.7.4-Setup.exe](https://github.com/L-lj67/Xingyu/releases/download/v0.7.4/Xingyu-0.7.4-Setup.exe)

也可以先查看 [v0.7.4 版本说明](https://github.com/L-lj67/Xingyu/releases/tag/v0.7.4)。

安装程序为 Windows x64 自包含版本，不要求另行安装 .NET。由于个人项目尚未购买商业代码签名证书，Windows 可能显示 SmartScreen 提示；请确认文件来自本仓库的正式 Release，并核对版本页提供的 SHA256。

## 快速开始

1. 点击“＋ 新建”创建项目。
2. 在下方工作区直接修改项目名称。
3. 在正文中自由输入，或粘贴图片、拖入附件。
4. 需要时再打开“属性”，设置状态、进度、优先级或提醒。
5. 右键软件标题可以调整外观、存在形式、快捷呼出与开机启动。

完整说明见 [使用指南](packaging/使用指南.txt)。

## 数据、隐私与卸载

行域当前完全在本机运行，不要求账号，不依赖云服务，也不会自动上传项目内容。安装时可以选择数据父目录，行域只在其中创建并管理专属的 `XingyuData` 文件夹。

右键软件标题选择“彻底卸载行域…”，或从 Windows“设置 → 应用 → 已安装的应用”卸载，可以删除程序、项目数据、设置、缓存、提醒、快捷方式和开机启动项。附件所引用的外部原始文件以及用户另行保存的安装程序不会被删除。

请自行备份重要数据。v0.7.4 尚未提供自动备份、项目导入导出或旧开发版本数据迁移。

## 从源代码运行

需要：

- Windows 10/11 x64
- .NET 8 SDK
- PowerShell

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\scripts\dev.ps1"
```

运行验证：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\scripts\verify.ps1"
```

生成自包含程序：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\scripts\publish.ps1"
```

生成安装包还需要安装 Inno Setup 7，然后运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File ".\scripts\build-installer.ps1"
```

## 项目状态与后续方向

v0.7.4 是首个公开版本，当前重点是稳定桌面端的自由书写、项目组织与窗口存在形式，而不是扩展成团队项目管理工具。

后续可能探索：

- 项目导入、导出与备份
- 将 AI / Agent 对话导入项目，并由用户摘录、评注和管理
- 独立嵌入式小屏幕上的行域终端
- 更多可选的桌面存在形态

这些方向是探索地图，不代表固定排期。详见 [未来方向](docs/FUTURE_DIRECTIONS.md) 与 [项目宪法](docs/PROJECT_CONSTITUTION.md)。

## 项目背景

行域起源于一次本科阶段的 Vibe-coding 实践：从对 Windows 便笺的反思开始，经过真实使用、伙伴测试和多轮产品讨论，逐渐形成“项目清单层 + 项目工作空间层”的两层模型。

它不以成为全能笔记软件为目标，而尝试回答一个更具体的问题：当一件事持续数天、数周甚至更久时，怎样让它的上下文始终留在一个可以继续行动的现场里？

## 许可证

本项目采用 [MIT License](LICENSE)。你可以使用、学习、修改、分发或销售本软件及其衍生版本，但必须保留原版权与许可证声明。软件按现状提供，不附带担保。
