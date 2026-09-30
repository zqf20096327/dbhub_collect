# MyBatis GaussDB Log Plugin

IntelliJ IDEA 插件，用于解析 MyBatis SQL 日志并还原为完整的可执行 SQL，支持 GaussDB 数据库。

## 功能特性

- 解析 MyBatis 控制台日志
- 将带参数占位符的 SQL还原为完整可执行 SQL
- 支持 GaussDB 特定的 SQL语法
- SQL格式化显示
- 可配置日志解析关键字

## 使用方法

1. 在 IntelliJ IDEA 中打开项目
2. 点击 Tools -> MyBatis GaussDB Log
3. 迒行应用程序，当控制台输出 MyBatis SQL 日志时，插件会自动解析并显示完整 SQL

## 构建

```bash
# Windows
gradlew.bat buildPlugin

# Linux/Mac
./gradlew buildPlugin
```

构建产物位于 `build/distributions/` 目录。

## 安装

1. 构建 plugin
2. 在 IntelliJ IDEA 中选择 File -> Settings -> Plugins -> Install Plugin from Disk
3. 选择构建的 zip 文件进行安装

## 项目结构

```
src/main/java/com/gaussdb/mybatislog/
├── BasicFormatter.java        # SQL格式化器
├── Icons.java                 # 图标定义
├── MyBatisLogConsoleFilter.java  # 控制台过滤器
├── MyBatisLogConsoleFilterProvider.java
├── action/                    # Action 类
│   ├── MyBatisLogAction.java
│   ├── ClearAllAction.java
│   ├── PrettyPrintToggleAction.java
│   ├── RerunAction.java
│   ├── StopAction.java
│   └── SettingsAction.java
├── gui/                       # GUI 相关
│   ├── MyBatisLogExecutor.java
│   └── MyBatisLogManager.java
```

## 参考

基于 [mybatis-log-plugin-free](https://github.com/starxg/mybatis-log-plugin-free) 项目实现。