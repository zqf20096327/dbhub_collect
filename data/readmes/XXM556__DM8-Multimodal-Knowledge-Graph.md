# 达梦多模态知识图谱系统

这是一个基于国产达梦数据库（DM8）和 Flask 开发的多模态工艺知识图谱存储与可视化平台。它支持自动解析上传的 PDF、图片、3D 模型等不同格式数据，构建结构化的关系网络，并在网页端提供原位预览和检索功能。

## 环境要求

1. **Python 3.8+**
2. **达梦数据库 (DM8)**
   - 需要在运行机器上安装并启动达梦数据库服务。
   - 需确保 `dmPython` 驱动能在该机器的 Python 环境下成功安装和运行。

## 部署与启动步骤

### 1. 克隆代码
将本项目代码克隆到本地机器上。

### 2. 配置环境变量
在项目根目录找到 `.env.example` 文件，将其复制一份并重命名为 `.env`。
然后打开 `.env` 文件，根据您的实际达梦数据库配置填写以下信息：
```env
DM_USER=SYSDBA
DM_PWD=your_database_password
DM_HOST=localhost
DM_PORT=5236
```
> **注意**：`.env` 文件已被 `.gitignore` 忽略，请不要将包含真实密码的 `.env` 提交到 GitHub 上。

### 3. 安装依赖
在项目根目录下，使用 pip 安装依赖包：
```bash
pip install -r requirements.txt
```

### 4. 初始化数据库
**如果是首次在这台机器上运行**，需要先初始化达梦数据库表结构：
在达梦数据库管理工具（或使用 `disql` 命令行工具）中，执行项目根目录下的 `init_multimodal_db.sql` 脚本。

该脚本会自动创建所需的 `DM_ENTITIES`、`DM_METADATA`、`DM_EXTRACTED_FEATURES`、`DM_KNOWLEDGE_RELATIONS` 表结构。

### 5. 启动 Flask Web 服务
运行以下命令启动服务：
```bash
python web_app.py
```
服务启动后，在浏览器中访问 `http://127.0.0.1:5000` 即可看到前端面板。

## 自定义关系类型
在首次运行或上传后，系统会在根目录生成一个 `relation_config.json` 文件。您可以自由编辑该文件来增加或修改知识图谱的连线关系类型，修改后刷新网页即可生效。