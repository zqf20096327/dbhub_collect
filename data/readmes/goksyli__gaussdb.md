# pthread_exit 卡住线程自动定位 Demo

由进程内 watchdog 检测退出超时，采集目标线程的寄存器和栈快照，定位 cleanup/TLS 析构中的业务函数。包含真实 pthread 退出故障注入、自动断言、原始诊断 JSON 和测试报告。

当前版本已在 **Linux x86_64** 编译和运行：基础测试 **25/25**，20 轮重复测试 **272/272**。除进程内信号采样外，Linux 还提供同 binary fork helper 的 ptrace 采样，可在线程屏蔽诊断信号时读取寄存器和 frame-pointer 链。

## 编译和运行

依赖：C++17 编译器、make、Python 3；源码行解析在 Linux 需要 binutils 的 `addr2line`，macOS 需要 Command Line Tools 的 `atos`。

```sh
cd /Users/goksyli/gaussdb
make all
./build/exit_watchdog_demo cleanup-lock
./build/exit_watchdog_demo tls-lock
DIAG_PTRACE_LOG=/tmp/ptrace.raw ./build/exit_watchdog_demo ptrace-signal-blocked
./build/stack_symbolize --input /tmp/ptrace.raw --binary ./build/exit_watchdog_demo
make test
make stress
```

复制到 Linux 后，在复制后的项目目录运行相同的 make 命令；不需要第三方 Python 包。Linux 可用 `make CXX=g++ test`，macOS 默认使用系统 `c++`。

输出为一行 JSON，包含线程 TID、退出入口和源码行、退出阶段、采样后端、原始 PC/SP/FP、业务函数栈、截断原因、超时结果及 Linux `/proc` 证据。`ptrace-signal-blocked` 由主进程在创建线程前 fork helper；helper 和主进程来自同一个 `exit_watchdog_demo` binary。helper 只将寄存器及 FP 链原始地址写入 `DIAG_PTRACE_LOG`，符号和源码行必须由额外的 `stack_symbolize` binary 离线解析。

Linux ptrace 受 Yama、seccomp、容器配置及进程凭据约束。demo 通过 `PR_SET_PTRACER` 精确授权 fork 出的 helper，不要求关闭全局 `ptrace_scope`；但禁止 ptrace 的沙箱仍需显式放行。生产接入必须在创建其他线程和加载复杂运行库前启动 helper，并保持最小权限。

Git 仓库保留源码、测试、设计文档、测试报告和 `summary.json`；逐次运行的原始 JSON/日志及编译产物保留在本地，可运行上述命令重新生成。

```text
__psynch_mutexwait
  _pthread_mutex_firstfit_lock_slow
    DemoLockWait
      DemoCleanupWait       <- 实际等待的业务路径
        DemoCleanupHandler
          _pthread_exit
            pthread_exit
```

上述为本机真实采样的简化栈。Linux 的系统库函数名不同，不应使用这段文本作为 Linux 的预期栈。

## 文档和测试产物

- [设计报告](docs/DESIGN.md)：架构、状态协议、平台差异、接入 GaussDB 的建议及实现边界。
- [测试总结](docs/TEST_REPORT.md)：验收结论、用例覆盖、已修复问题和未验证项。
- [基础测试自动报告](artifacts/test/TEST_REPORT.md)：25 项实际结果、实际堆栈和源码行。
- [重复测试自动报告](artifacts/stress/TEST_REPORT.md)：272 项实际结果。
- [基础测试机器可读结果](artifacts/test/summary.json)、[重复测试机器可读结果](artifacts/stress/summary.json)：环境、耗时、源码/二进制 SHA-256。

## 可选场景

```text
cleanup-lock       tls-lock          return-tls-lock
normal-exit        normal-return     running-wait
slow-cleanup       signal-blocked    late-signal
truncated-stack    repeated-capture  signal-live
ptrace-signal-blocked (Linux)
```

`make test` 运行全部场景一次；`make stress` 每个集成场景重复 20 次。自定义轮数：

```sh
python3 tests/run_tests.py --repeat 5 --output artifacts/custom
```

每次测试使用独立进程，超时 8 秒；诊断后由锁持有者释放测试锁，再 join 目标线程。没有强行结束线程，也没有修改 mutex 内部结构。

这是单目标、joinable 线程的诊断原型，不是已经接入 GaussDB 的补丁。真实退出采样在 Linux 可使用 `tgkill` 信号或 fork ptrace helper，在 macOS 使用 Mach 快照；macOS 的信号协议用例在调用 `pthread_exit` 前执行，原因见设计报告。DWARF 完整展开、多目标注册表和锁 owner 自动追踪尚未实现。
