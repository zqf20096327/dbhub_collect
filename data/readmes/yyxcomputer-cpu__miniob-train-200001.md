# MiniOB 训练营 200001 数据库内核实验

目标训练营：https://open.oceanbase.com/train/detail/3?questionId=200001  
实验分支：`train-200001`  
实验报告：[docs/experiment-report.md](docs/experiment-report.md)  
实现范围与局限：[docs/course-200001.md](docs/course-200001.md)

本项目基于官方源码新增独立服务入口 `src/observer/course_main.cpp`，在 `src/observer/sql/native` 实现原生 C++14 SQL 与存储内核。
运行时不调用外部数据库。索引使用内存有序复合键，存储使用目录快照；具体取舍见报告。

## 构建与验证

建议使用 Linux 或官方 `oceanbase/miniob` 开发镜像。Ubuntu 22.04 可安装
`build-essential cmake libevent-dev libjsoncpp-dev python3`，并执行：

```sh
export CPLUS_INCLUDE_PATH=/usr/include/jsoncpp
cmake -S . -B build -DWITH_UNIT_TESTS=OFF
cmake --build build --target observer -j 4
python3 test/course/public_cases.py --observer build/bin/observer --results public-results
python3 test/course/edge_cases.py --observer build/bin/observer --results edge-results
g++ -std=c++14 test/course/unix_smoke.cpp -o build/unix-smoke
python3 test/course/startup_cases.py --observer build/bin/observer --unix-client build/unix-smoke --results startup-results
```

CMake 4 如提示旧项目最低版本不兼容，可在配置时加 `-DCMAKE_POLICY_VERSION_MINIMUM=3.5`。
服务器可用 `build/bin/observer -f etc/observer.ini -p 6789` 启动；Unix Socket 使用 `-s /tmp/miniob.sock`。
SQL 请求和响应均以空字节结尾，不能用普通换行代替协议分隔符。

公开结果：18/18 套、1074 条 SQL 通过；另有 584 项检查和 4 种启动组合通过。
线上已通过 18/18 题，240/240 分，记录编号 **47253992**。
评测提交：`89dcf1df5db949cba2d493d5de70b9ece9de3e75`。
[逐题记录](docs/online-result.json)；自动化验证在仓库 Actions 中运行。

默认入口直接提供兼容 MiniOB 的 TCP/Unix Socket 协议，不依赖旧 SEDA 共享框架。
原 SEDA 入口仍可通过 `-DCOURSE_NATIVE_SERVER=OFF` 构建，作为保留的集成方式。

以下保留官方项目原始介绍与许可证。

---

# 介绍
miniob 是 OceanBase 与华中科技大学联合开发的、面向"零"基础同学的数据库入门实践工具。
miniob 设计的目标是让同学们快速了解数据库并深入学习数据库内核，期望通过相关训练之后，能够对数据库内核各个模块的功能及其关联有所了解，并能够在
使用数据库时，设计出高效的 SQL 。miniob 面向的对象主要是在校学生，并且诸多模块都做了简化，比如不考虑并发操作。

(注意：此代码仅供学习使用，不考虑任何安全特性。)

[GitHub 首页](https://github.com/oceanbase/miniob)

# 1. 题目说明
[miniob 题目描述](docs/miniob_topics.md) 

# 2. 开发指南
## 搭建开发环境
1. [本地配置gcc环境](docs/how_to_build.md)。
2. [使用Docker开发](docs/how-to-dev-using-docker.md)。
3. [在Windows上使用Docker](docs/how_to_dev_miniob_by_docker_on_windows.md)。

## 词法、语法解析
请参考 [miniob 词法语法解析开发与测试](docs/miniob-sql-parser.md)。

# 3. 提交测试
题目完成并通过自测后，大家可以在 [miniob 训练营](https://open.oceanbase.com/train?questionId=200001) 上提交代码进行测试。

客户端输出需要满足一定要求，如果你的测试结果不符合预期，请参考 [miniob 输出约定](docs/miniob-output-convention.md)。

# 4. 数据库管理系统实现基础讲义
由华中科技大学谢美意和左琼老师联合编撰的数据库管理系统实现教材：[《数据库管理系统实现基础讲义》](docs/lectures/index.md)

# 5. miniob 介绍
[miniob 源码解析视频](https://open.oceanbase.com/activities/4921877)

[miniob 源码解析文档](https://www.oceanbase.com/docs/community-developer-quickstart-10000000000627363)

（资料持续整理中，请大家自行查阅标题为“MiniOB...”的视频或文档）
