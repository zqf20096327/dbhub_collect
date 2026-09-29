# 让手，变成声音

**打不了电话的人，做一个手势，它替他说话。**

VentureD × TiDB 智能硬件黑客松 · Physical AI 硬件赛道 · 第 19 组

---

## 这是什么

一台随身设备。板载摄像头看使用者的手，板上识别出手势，
Agent 把没有语序的词串重建成一句自然的中文，再由板载 TTS 念出来
给一个听得见的人听。

```
🤙 打电话  +  👍 要
        ↓
设备出声：「麻烦帮我打个电话，谢谢。」
```

「麻烦」和「谢谢」不在词串里，是 Agent 补的。
**这一步是判断，不是查表** —— 同样两个词，在医院和在便利店说法不一样。

![架构图](docs/architecture.png)

整条链路只有一步要联网（Agent 那一步）。
**识别在板上，语音合成也在板上，上云的只有几个词 —— 不是视频，不是声音。**

## 怎么跑起来

### 板子（这是现场跑的那一套）

硬件：ESP32-S3 AIoT Basic 板卡 A（145 × 135 mm）+ GC2145 摄像头 + ES8311 + LCD

```bash
cd firmware/camera_stream
idf.py set-target esp32s3
idf.py menuconfig      # 「板卡 A 摄像头视频流」里填 WiFi 和 Agent Stack 凭证
idf.py build flash monitor
```

> ⚠️ 分区表变过，**必须同时烧 bootloader + 分区表 + app + 模型**，
> 只烧 app 会报 `No bootable app partitions`。用 `idf.py flash`，不要手动只烧一个分区。

细节见 [`firmware/camera_stream/README.md`](firmware/camera_stream/README.md)。

### 外壳（可选，3D 打印）

```bash
cd case && python3 tray.py && python3 cover.py && python3 stand.py
```

STL 直接可打。托盘已经打出来装上了，盖子还没打。
见 [`case/README.md`](case/README.md)。

### web/（不是现场跑的）

板外识别的早期原型 + 调试工具：浏览器里跑 MediaPipe 做手势分割和 DTW 模板匹配，
Node 端做 Agent 代理、纠错学习和播报队列。
**识别搬到板上之后它不参与现场演示了**，留在这里是因为里面的 Agent 提示词设计、
纠错学习和分割算法还在用。

第三方 WASM 和模型文件（约 47 MB）没入库，见 [`web/README.md`](web/README.md) 的获取方式。

## 交付物

| | |
|---|---|
| 一句话 + 用户场景 + 团队 | [`docs/submission.md`](docs/submission.md) |
| 一页架构图 | [`docs/architecture.png`](docs/architecture.png) |
| Agent Stack 使用说明 | [`docs/agent-stack.md`](docs/agent-stack.md) |
| 硬件实测记录 | [`docs/HARDWARE.md`](docs/HARDWARE.md) |
| 演示视频 | 见提交表单 |

## 边界

主动说清楚我们没做到什么：

- **这不是手语翻译。** 现在识别的是九个通用手势（数字 1–5、点赞、踩、OK、打电话）。
  真正的手语有五千六百多个词、有国标 GF 0020—2018、有自己的语法和空间关系，
  甚至面部表情本身也是语法的一部分。**那是方向，不是现状。**
- **不看表情。**
- **端到端 7–9 秒**，不是实时。平台只有一个模型可选，而且没有系统提示字段，
  约束必须每轮重发。我们从 12 秒压到 7 秒，再往下不在我们这边。
- **认不准时它不出声。** 屏幕出 `?`，设备保持沉默 ——
  在医院、药物、求助这些场景里，说错比不说更危险。

仓库里只放了现场在跑的那一套。中间还有几版走过的路
（板外识别、传感器方案）留在私有仓库里，没有价值就不往这儿搬。

## 团队

**宋子钇** · 纽约大学计算机工程系 · 宾夕法尼亚大学研究生毕业 ·
沃顿商学院创业大赛 最佳设计 / 最佳想法

**刘通** · 前 Kimi 音视频工程师 · 十年一线大厂工程师 · 正在创业

## 凭证

赛事明文规定 API Key 不得出现在代码、视频或文档中。

- 凭证通过 `idf.py menuconfig` 填入，落在 `sdkconfig`，而 `sdkconfig` 在 `.gitignore` 里
- `.gitignore` 另外覆盖 `.env` / `*.key` / `*.pem`
- 本仓库全部内容与提交历史均扫描过，无密钥
