# 基于大模型和GaussDB的智能总结项目

本项目是一个基于PostgreSQL（GaussDB兼容）和DeepSeek API的问答系统，用户可以提出自然语言问题，系统会自动生成SQL查询，查询数据库，并基于结果给出自然语言回答。

## 项目结构
```bash
./
├── code/
│   ├── idsum.csv                     # 第一个表数据文件（id, summary）
│   ├── 视频1_summary_output.csv      # 第二个表数据文件（video_id=1）
│   ├── 视频2_summary_output.csv      # 第二个表数据文件（video_id=2）
│   ├── setup.py                      # 数据库初始化和数据插入脚本
│   └── main.py                       # 主程序，实现问答交互
├── README.md
├── example.txt                   # 示例问题文本
```

## 环境依赖

请确保已安装以下Python库：

```bash
pip install psycopg2 openai
```

或使用conda
```bash
conda install psycopg2 openai
```

## 运行指南

一、数据库初始化

运行 setup.py，用于创建数据库和表，并从CSV文件中读取数据插入数据库：

```bash
python code/setup.py
```

确保你已正确设置数据库连接信息，例如主机、端口、用户名、密码等。

二、运行问答主程序

运行 main.py 启动问答系统，输入自然语言问题，系统将自动完成：
1.使用 DeepSeek API 生成 SQL 查询语句
2.执行查询并获取结果
3.使用 DeepSeek 再次生成自然语言回答
    
```bash
python code/main.py
```

确保你已正确设置DeepSeek API Key及数据库连接相关信息。

三、DeepSeek API 配置说明

本项目使用 OpenAI SDK 调用 DeepSeek API（兼容）

你需要替换 main.py 中的 api_key 为你申请的 DeepSeek API Key

使用 DeepSeek Chat 模型：model='deepseek-chat'

API Base URL：https://api.deepseek.com

四、常见问题

请确保你的csv文件均使用utf-8进行编码。

五、联系方式

如有疑问，请联系bowen20041225@sina.com。

本项目为北京师范大学人工智能学院2024-2025学年度春季学期数据库系统课程（党德鹏教授）大作业，组号为第一组。

六、许可

如果你发现本项目对你的研究有帮助，你可以在非赢利目的下使用本项目，但请引用本项目。

但是，抄袭是被学术规范所拒绝的，请不要将本项目直接作为你的任何课程作业提交。
