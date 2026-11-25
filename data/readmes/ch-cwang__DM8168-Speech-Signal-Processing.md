# 基于 DM8168 的异构多核语音信号处理

基于 TI DM8168（ARM Cortex-A8 + DSP C674x）的双核音频处理系统。ARM 运行 Linux，负责调度、ALSA I/O 和音频块管理；DSP 运行 SYS/BIOS，负责 Q15 空间音效卷积。PCM 数据始终位于 SharedRegion 中，TX 与 RX 各用一个共享 `head/tail` 环形索引结构同步；Notify 只用于启动、握手和关机等控制事件。

## 数据流

```
采集(ADC) → ARM 录制线程 → 共享内存 TX ring → TX.head
         → DSP 双耳 FIR → 共享内存 RX ring → RX.head
         → ARM 播放线程 → 播放(DAC) → RX.tail
```

## 系统架构

```
外部音频编解码器 (ADC/DAC)
        │  I2S / DMA
        ▼
ARM Cortex-A8 (Linux)
  main_host.c / App.c
  录制线程 · 播放线程
        │  SharedRegion: PCM blocks + SPSC queues
        ▼
共享内存 SR1
  TX ring head/tail + 20 × 2 KB 录制区
  RX ring head/tail + 20 × 4 KB 播放区
        ▲
        │  SharedRegion; Notify only for control
DSP C674x (SYS/BIOS)
  main_dsp.c / Server.c
  无锁消费循环 + Q15 双耳 FIR
```

## 功能特性

- 音频规格：44.1 kHz，单声道采集、双声道播放，16 位小端（S16_LE），每块 1024 帧。
- 空间音效：512 阶左右耳 HRIR，Q15 定点、40 位累加、饱和截断。
- 零拷贝通信：PCM 数据仅在共享内存中传递，核间只传递块索引。
- 无锁数据面：TX、RX 各一个共享 `head/tail` 环；消费者推进 `tail` 即自动归还数据块。
- 本版本不启用冷热分层：HRIR 仍使用默认链接位置，没有 `.hrir_sram` 或 OCMC 放置。
- ARM 使用 `__sync_synchronize()`；DSP 侧沿用共享区 no-cache 与 volatile 访问方式。
- 空闲轮询采用短自旋后休眠：ARM 等待 50 微秒，DSP 等待 1 个 BIOS tick。
- 双缓冲环形队列：录制与播放各 20 块，缓冲深度共 400 ms，用于吸收 Linux 调度抖动。
- 抗撕裂拼装：对 ALSA 分段返回的残缺数据按 1024 帧强制拼装，避免音频帧错位。
- 播放预充水：播放启动阈值设为 3 个周期，避免冷启动爆音与欠载。
- 优雅退出：ARM 与 DSP 通过控制消息握手退出，安全释放共享内存和 ALSA 句柄。

## 目录结构

- `host/`：ARM 端应用源码，含 `main_host.c`、`App.c`。
- `dsp/`：DSP 端固件源码，含 `main_dsp.c`、`Server.c`、`Dsp.cfg`。
- `shared/`：双核共享头文件，含 `AppCommon.h`、`SystemCfg.h`。
- `tests/`：自动化测试脚本与测试计划。
- `docs/`：需求、设计、测试报告文档。

## 环境依赖

- SYS/BIOS（TI-RTOS kernel）
- XDCtools
- SysLink / IPC
- CGT ARM（交叉编译器，如 `arm-none-linux-gnueabi`）
- CGT C6000（DSP 编译器）

## 编译与运行

1. 将 `products.mak.example` 复制为 `products.mak`，按实际安装路径修改。
2. 在项目根目录执行 `make` 构建，再执行 `make install` 生成 `install/`。
3. 将 `install/` 拷贝到开发板（ARM Linux），执行 `./run.sh` 启动系统。
4. 控制台出现运行提示后，按回车键触发优雅退出。

## 测试

测试脚本位于 `tests/`：

- `test_case1_basic.sh`：基础连通性测试。
- `test_case2_stress.sh`：CPU 高负载抗撕裂测试。
- `test_case3_ipc_lifecycle.sh`：频繁启停防死锁测试。
- `setup_alsa_snoop.sh`：ALSA 旁路抓包。

## 文档

- [需求规格说明](docs/requirements.md)
- [系统设计说明](docs/system_design.md)
- [软件测试报告](docs/software_test_report.md)
- [音频测试计划](tests/audio_test_plan.md)

## 许可证

BSD-3-Clause。
