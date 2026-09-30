# DBSyncLocal

一个从达梦数据库读取数据并保存到本地的一个软件

## 功能特性

- 连接达梦数据库(DM Database)
- 从达梦数据库读取表数据
- 将数据映射保存到本地SQLite数据库
- 在UI界面中显示和编辑数据
- 用户修改数据后自动更新本地数据库
- 支持从远端数据库重新加载数据(覆盖本地)

## 系统要求

- 操作系统: 麒麟V10 (Kylin V10)
- Qt版本: Qt 5.12
- 达梦数据库驱动 (需要安装)

## 编译步骤

1. 安装Qt 5.12开发环境
2. 安装达梦数据库客户端库
3. 配置达梦数据库驱动路径(修改DBSyncLocal.pro文件)
4. 编译项目:

```bash
cd DBSyncLocal
qmake
make
```

## 配置达梦数据库驱动

在编译前,需要配置达梦数据库驱动路径。编辑 `DBSyncLocal.pro` 文件,取消注释并修改以下行:

```qmake
# INCLUDEPATH += /path/to/dm/include
# LIBS += -L/path/to/dm/lib -ldm
```

将路径替换为实际的达梦数据库安装路径。

## 使用方法

1. 运行程序: `./DBSyncLocal`
2. 点击"配置"按钮,输入达梦数据库连接信息
3. 点击"连接数据库"按钮连接到达梦数据库
4. 选择要同步的表
5. 点击"加载远程数据"按钮从达梦数据库加载数据到本地
6. 在表格中查看和编辑数据,修改会自动保存到本地数据库
7. 再次点击"加载远程数据"会用远端数据覆盖本地数据

## 项目结构

```
DBSyncLocal/
├── src/
│   ├── main.cpp              # 主程序入口
│   ├── mainwindow.h/cpp      # 主窗口类
│   ├── mainwindow.ui         # UI界面文件
│   ├── dmdatabase.h/cpp      # 达梦数据库操作类
│   ├── localdatabase.h/cpp   # 本地SQLite数据库操作类
│   └── datamodel.h/cpp       # 数据模型类
├── config/
│   └── config.ini            # 配置文件(运行时生成)
├── DBSyncLocal.pro           # Qt项目文件
└── README.md                 # 本文档
```

## 数据库表结构

本地SQLite数据库包含以下表:

- `table_mapping_info`: 存储表映射信息
  - id: 主键
  - table_name: 表名
  - source_table: 源表名
  - last_sync_time: 最后同步时间

- 用户表: 每个从达梦数据库同步的表会在本地创建对应的映射表
  - id: 主键(自增)
  - 其他列: 根据源表结构创建

## 注意事项

1. 达梦数据库驱动需要单独安装,Qt默认不包含达梦数据库驱动
2. 首次运行时需要在配置界面输入数据库连接信息
3. 本地数据库文件为 `local_mapping.db`,位于程序运行目录
4. 用户编辑数据会实时保存到本地数据库
5. 点击"加载远程数据"会用远端数据完全覆盖本地数据

## 开发环境

- Qt 5.12
- C++11
- SQLite 3
- 达梦数据库客户端库

## 许可证

MIT License

## 作者

jiangzhuo88