# 上位机数据采集监控系统

一个用于学习和求职演示的 C# 上位机项目，基于 WPF + Modbus TCP + SQLite。

## 功能

- WPF 界面实时显示寄存器数据
- 手写 Modbus TCP 请求与响应解析
- 读取保持寄存器，写入单个寄存器
- 后台定时轮询，不阻塞 UI
- SQLite 保存历史数据和报警记录
- 高限 / 低限报警判断与去重
- 实时趋势曲线
- 内置 Modbus TCP 模拟从站，无需真实硬件

## 项目结构

```text
UpperMachineDemo/
    Models/          数据模型
    Services/        Modbus 客户端、轮询服务、SQLite 服务
    MainWindow.xaml  WPF 主界面
ModbusTcpSimulator/
    Program.cs       Modbus TCP 模拟从站
```

## 运行方式

1. 用 Visual Studio 打开解决方案
2. 同时启动 `UpperMachineDemo` 和 `ModbusTcpSimulator`
3. 模拟器监听 `127.0.0.1:502`
4. WPF 程序点击“连接”
5. 点击“开始轮询”观察数据自动刷新、趋势曲线和报警记录

## 核心技术

- C# / .NET 10
- WPF / XAML
- TcpClient / Modbus TCP
- async / await 后台轮询
- Microsoft.Data.Sqlite
- Git / NuGet
