name: changshu-dev-assistant-integration
version: 1.0.0
description: 昌叔专属软件开发助手集成模块 - 测试自动化功能增强
author: Hermes Agent
tags: [dev, assistant, integration, testing]

# 昌叔专属软件开发助手集成模块

## 概述

这是昌叔专属软件开发助手的集成模块，专注于提供测试自动化功能增强。

## 核心功能

### 1. 测试用例生成
- 自动生成基于源代码的测试用例
- 支持pytest和unittest框架
- 支持类和函数的测试用例生成

### 2. 测试运行
- 集成pytest和unittest测试运行器
- 提供详细的测试报告
- 支持多种测试框架

### 3. 覆盖率分析
- 分析测试覆盖率
- 提供覆盖率改进建议
- 识别未覆盖的代码区域

## 使用方法

### 命令行使用
```bash
# 生成测试用例
changshu-assistant test-generate --file <source_file> --type <framework>

# 运行测试
changshu-assistant test-run --file <test_file> --type <framework>

# 分析测试覆盖率
changshu-assistant test-analyze --file <source_file> --test-file <test_file>
```

### 配置
在config.yaml中添加以下配置:
```yaml
features:
  test_automation: true

testing:
  frameworks:
    - pytest
    - unittest
```

## 技术实现

### 测试生成器
- 基于AST解析源代码
- 自动生成测试模板
- 支持类和函数的测试用例生成

### 测试运行器
- 集成主流测试框架
- 提供详细的测试报告
- 支持覆盖率分析

### 覆盖率分析
- 分析代码覆盖率
- 识别未覆盖的代码区域
- 提供覆盖率改进建议

## 配置说明

在昌叔助手的主配置文件中添加测试自动化配置:
```yaml
features:
  test_automation: true

testing:
  frameworks:
    - pytest
    - unittest
```

## 使用场景

### 日常开发
```bash
# 生成测试用例
changshu-assistant test-generate --file app.py --type pytest

# 运行测试
changshu-assistant test-run --file test_app.py --type pytest

# 分析覆盖率
changshu-assistant test-analyze --file app.py --test-file test_app.py
```

## 常见问题

### Q: 如何生成测试用例？
A: 使用`changshu-assistant test-generate --file source_file.py --type pytest`命令生成测试用例。

### Q: 如何运行测试？
A: 使用`changshu-assistant test-run --file test_file.py --type pytest`命令运行测试。

### Q: 如何分析测试覆盖率？
A: 使用`changshu-assistant test-analyze --file source_file.py --test-file test_file.py`命令分析测试覆盖率。

## 更新日志

### v1.0.0 (2026-05-17)
- 初始版本发布
- 测试用例生成功能
- 测试运行功能
- 覆盖率分析功能