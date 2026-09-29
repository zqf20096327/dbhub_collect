# DeviceMonitor

基于 C#、WPF、MVVM、Modbus TCP 和 SQLite 开发的工业设备监控上位机。

## 技术栈

- .NET 8
- WPF
- MVVM
- NModbus
- Entity Framework Core
- SQLite
- LiveCharts2
- Serilog
- xUnit

## 项目结构

- DeviceMonitor.App：WPF 上位机
- DeviceMonitor.Core：通信、业务、数据库
- DeviceMonitor.Simulator：Modbus TCP 设备模拟器
- DeviceMonitor.Tests：单元测试

## 核心功能

- Modbus TCP 设备通信
- 实时数据采集与自动重连
- 设备启动和停止控制
- 温度报警阈值下发
- 历史数据与报警记录
- 实时温度、压力趋势
- CSV 数据导出
- EF Core Migration
- Serilog 文件日志
- xUnit 报警业务测试

## Modbus 寄存器

| 地址 | 含义              |
| ---- | ----------------- |
| 0    | 运行状态          |
| 1    | 温度 × 10         |
| 2    | 压力 × 100        |
| 3    | 总产量            |
| 4    | OK 数量           |
| 5    | NG 数量           |
| 6    | 报警码            |
| 7    | 设备启停命令      |
| 8    | 温度报警阈值 × 10 |

## 运行方式

1. 使用 Visual Studio 2022 打开 `DeviceMonitor.sln`。
2. 启动 `DeviceMonitor.Simulator`。
3. 启动 `DeviceMonitor.App`。
4. 使用 `127.0.0.1:1502`、站号 `1` 连接模拟设备。