# MiniMax × OceanBase 赛题：SDD上下文管理助手

## 项目简介
本项目实现了面向Spec-Driven Development（规格驱动开发）的AI开发助手上下文模块，完成了题目要求的全流程：
1. 导入业务代码与开发任务规格
2. 基于上下文调用MiniMax模型完成实际代码修改
3. 运行测试验证修改正确性
4. 持久化保存任务状态，支持重启后恢复开发进度

## 技术实现
- **AI代码修改**：使用MiniMax abab6.5s模型完成代码生成与修改
- **代码上下文存储**：本地JSON文件模拟seekdb/OceanBase存储业务代码与规格资料
- **任务状态管理**：本地JSON文件模拟PowerContext保存开发任务进度，支持断点续跑
- **业务场景**：Python待办列表TodoList项目，为其增加删除任务的功能

## 运行步骤
1. 安装依赖：`pip install -r requirements.txt`
2. 把`sdd_assistant.py`里的`YOUR_MINIMAX_API_KEY`替换成你自己的MiniMax API Key
3. 运行程序：`python sdd_assistant.py`

## 验证样例
程序会自动完成以下验证流程：
✅ 导入TodoList业务代码与开发需求
✅ 调用MiniMax自动为TodoList增加`delete_task`删除功能
✅ 运行`test_todo.py`验证原有功能不被破坏
✅ 保存任务状态，模拟重启后读取开发进度

## 提交材料清单
- [x] 源码仓库（本目录所有Python代码）
- [x] 运行说明（本README）
- [x] 验证样例（test_todo.py测试用例）
- [x] 技术使用记录（本项目完整使用了MiniMax API、上下文存储、任务状态管理）
