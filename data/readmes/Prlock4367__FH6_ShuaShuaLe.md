<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/PySide6-6.11.1-brightgreen.svg" alt="PySide6">
  <img src="https://img.shields.io/badge/OpenCV-4.13.0.92-blue.svg" alt="OpenCV">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="License">
  <img src="https://img.shields.io/github/v/release/Prlock4367/FH6_ShuaShuaLe?color=red&label=version" alt="Version">
  <img src="https://img.shields.io/github/downloads/Prlock4367/FH6_ShuaShuaLe/total?color=success" alt="Downloads">
</p>

<h1 align="center">
  🏎️ FH6_ShuaShuaLe
</h1>

<p align="center">
  <strong>《极限竞速：地平线 6》自动化辅助工具</strong><br>
  刷技术点 · 超级抽奖 · 综合循环刷 · 送外卖 · 刷劲敌 · 线上挂机 · 遥测监控
</p>

<p align="center">
  <a href="https://www.bilibili.com/video/BV1RbEJ6fE6g">📺 B站视频教程</a> ·
  <a href="https://www.xiaoheihe.cn/app/bbs/link/182618437">📖 小黑盒攻略</a> ·
  <a href="https://github.com/Prlock4367/FH6_ShuaShuaLe/releases">⬇️ 下载 Release</a> ·
  <a href="https://ifdian.net/a/Prlock">☕ 爱发电赞助</a>
</p>

---

## ✨ 功能一览

- 🎯 **刷技术点** — 图像识别/纯按键双模式，自动重开比赛
- 🎰 **刷超级抽奖** — 完整买车+抽奖循环，失败即停
- 🔄 **综合循环刷** — 多步流程串联，独立参数配置，实时步骤高亮
- 🍔 **送外卖** — 遥测模式（推荐）/ 图像识别 / 纯按键三种模式
- 🏁 **刷劲敌** — 辅助驾驶全自动挂机（防掉线）
- 🌐 **线上挂机** — 线上自定义比赛无碰撞模式，自动防掉线
- 🏆 **排行榜** — 6 个独立榜单，仅上传程序内数据，不涉及个人隐私
- 📊 **遥测监控** — UDP 实时显示 80+ 数据字段

> 📖 **详细操作步骤、蓝图代码、车辆调教、游戏内设置请查看 [小黑盒教程帖](https://www.xiaoheihe.cn/app/bbs/link/182618437)**

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.11+ | 主体语言 |
| PySide6 | GUI 框架 |
| PySide6-Fluent-Widgets | Fluent Design 组件，Windows 11 风格 |
| OpenCV | 图像识别与模板匹配 |
| windows-capture | 高性能 DirectX 窗口截图 |
| pywin32 | Windows API，后台按键模拟 |
| Flask + Gunicorn | 排行榜服务端框架及部署 |
| SQLAlchemy + MySQL | 排行榜数据持久化 |

---

## 📦 快速开始

```bash
git clone https://github.com/Prlock4367/FH6_ShuaShuaLe.git
cd FH6_ShuaShuaLe
pip install -r requirements.txt
python main.py
```

---

## 🔧 环境要求

- Windows 10/11（建议 1903+）
- 《极限竞速：地平线 6》已运行，窗口标题为 `Forza Horizon 6`
- 游戏键位保持默认，关闭"下一站"设置
- 需安装 [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)（x64）

---

## ❓ 常见问题

- **找不到窗口**：以管理员身份运行，检查游戏窗口标题是否为 `Forza Horizon 6`
- **图像识别失败**：运行画面校准，确保游戏窗口客户区为 1280x720
- **遥测模式绑定失败**：检查游戏内 UDP 遥测输出是否开启（端口 1000），微软商店版需解除网络限制
- **启动闪退**：查看 `fh6_tool.log` 日志，确认 VC++ 运行库已安装

---

## 🧪 后续计划

- 🔄 漂移辅助（过三星）
- 🔄 更多自动驾驶场景

## ☕ 赞助支持

如果这个工具对你有帮助，可以请作者喝杯咖啡。赞助全部用于项目维护，也是我持续更新的动力。

👉 [前往爱发电支持 Prlock](https://ifdian.net/a/Prlock)

---

## 📞 反馈与交流

- **GitHub Issues**：[提交 Bug / 需求建议](https://github.com/Prlock4367/FH6_ShuaShuaLe/issues)
- **小黑盒**：[教程帖留言](https://www.xiaoheihe.cn/app/bbs/link/182618437)（附截图 + 日志）
- **B站**：[视频教程下方评论](https://www.bilibili.com/video/BV1RbEJ6fE6g)

---

## ⭐ Star 趋势

<img src="https://api.star-history.com/svg?repos=Prlock4367/FH6_ShuaShuaLe&type=Date" width="500" alt="Star History">

---

## 📄 许可证

本项目采用 **MIT License** 开源，详情见 [LICENSE](LICENSE) 文件。

---

## ⚠️ 免责声明

本工具仅供学习交流，与《地平线 6》官方无关。仅模拟键盘操作，不修改游戏内存。使用第三方辅助工具存在账号风险，请自行判断并承担后果。禁止用于商业用途或破坏公平环境。

---

<p align="center">Made with ❤️ by Prlock</p>
