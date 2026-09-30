# Oceanbase charset tables

OceanBase 字符集表库

## 简介

本项目提供 OceanBase 数据库所需的字符集表数据和相关功能支持。

## 构建

### 依赖

- CMake 3.12.2 或更高版本
- GCC/G++ (支持 C++11)

### 编译步骤

```bash
bash build.sh debug/release
cd build_debug/build_release
make
```

### 安装包构建
```bash
bash rpm/devdeps-obcharset-build.sh
```

## 项目结构

```
.
├── lib/              # 库源代码
├── CMakeLists.txt    # CMake 构建配置
└── README.md         # 项目说明文档
```

## 许可证

请参考项目许可证文件。
