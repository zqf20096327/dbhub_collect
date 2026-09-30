# OCR 识别结果预览工具

快速预览 OCR 识别结果及原始文件内容。

## 功能

- 表格展示识别记录（文件信息、识别状态、结果）
- 点击行展开查看：原始文件预览 + 识别结果 JSON
- 支持图片/PDF 预览
- 支持按状态筛选、搜索文件名

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 准备数据（两种方式）
# 方式A：从 Oracle 导出为 JSON
python scripts/export_from_oracle.py > data/records.json

# 方式B：手动创建 data/records.json

# 3. 启动服务
python app/main.py

# 4. 浏览器打开 http://localhost:8080
```

## 数据格式

`data/records.json`：
```json
[
  {
    "id": 1,
    "scan_result_id": "scan_001",
    "file_name": "doc1.jpg",
    "file_path": "/path/to/file",
    "file_content": "base64或URL",
    "page_number": 1,
    "extraction_result": "{\"text\": \"...\"}",
    "extraction_status": "SUCCESS",
    "recognition_result": "{\"fields\": {...}}",
    "recognition_status": "SUCCESS",
    "mis_leading_status": 0,
    "create_time": "2026-03-03 10:00:00"
  }
]
```

## Oracle 导出脚本

```python
# scripts/export_from_oracle.py
import cx_Oracle
import json

conn = cx_Oracle.connect("user/pass@host/service")
cursor = conn.cursor()
cursor.execute("SELECT * FROM your_table WHERE ROWNUM <= 1000")
columns = [col[0] for col in cursor.description]
rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
print(json.dumps(rows, default=str, ensure_ascii=False))
```
