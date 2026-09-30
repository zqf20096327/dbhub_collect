# MySQL到DM8数据库迁移工具

这是一个用于将MySQL数据库迁移到DM8数据库的工具。该工具支持表结构（DDL）和数据（DML）的迁移，并提供了多种功能来确保迁移的准确性和可靠性。

## 主要功能

1. **表结构迁移**
   - 自动转换MySQL表结构为DM8兼容格式
   - 支持主键、外键、索引等约束
   - 自动处理数据类型映射

2. **数据迁移**
   - 支持大数据量迁移
   - 多线程并行处理
   - 自动处理字符编码问题
   - 错误数据自动记录和跳过

3. **错误处理**
   - 自动检测并记录乱码数据
   - 详细的错误日志记录
   - 错误数据单独保存，方便后续处理

4. **性能优化**
   - 批量数据处理
   - 多线程并行执行
   - 自动跳过问题数据，保证迁移效率

## 环境要求

- Python 3.8+
- MySQL 5.7+
- DM8 数据库
- 必要的Python包（见requirements.txt）

## 安装

1. 克隆项目到本地
2. 创建虚拟环境（推荐）：
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 配置

在`config`目录下创建`config.json`文件，配置数据库连接信息：

```json
{
    "mysql": {
        "host": "localhost",
        "port": 3306,
        "user": "your_mysql_user",
        "password": "your_mysql_password",
        "database": "your_mysql_database"
    },
    "dm8": {
        "host": "localhost",
        "port": 5236,
        "user": "your_dm8_user",
        "password": "your_dm8_password",
        "database": "your_dm8_database"
    }
}
```

## 使用方法

1. **基本用法**：
   ```bash
   python src/main.py --config path/to/config.json
   ```

2. **指定表范围**：
   ```bash
   python src/main.py --config path/to/config.json --start-table table1 --end-table table2
   ```

3. **查看帮助**：
   ```bash
   python src/main.py --help
   ```

## 输出说明

- `ddl/`: 存放生成的DDL文件
- `dml/`: 存放生成的DML文件（CSV格式）
- `error_data/`: 存放迁移过程中的错误数据
- `logs/`: 存放运行日志

## 注意事项

1. 确保有足够的磁盘空间存储中间文件
2. 建议在迁移前备份目标数据库
3. 对于大表，建议使用`--start-table`和`--end-table`参数分批迁移
4. 迁移完成后检查`error_data`目录中的错误数据

## 错误处理

1. 乱码数据会自动记录到`error_data`目录下的CSV文件中
2. 每条错误数据都包含原始数据和错误原因
3. 可以通过错误数据文件进行后续的数据修复

## 性能优化建议

1. 根据服务器配置调整`thread_pool_size`参数
2. 对于大表，可以适当调整`batch_size`参数
3. 建议在低峰期进行迁移操作

## 常见问题

1. **字符编码问题**
   - 工具会自动检测并记录乱码数据
   - 错误数据会保存在`error_data`目录中

2. **数据类型转换**
   - 自动处理MySQL和DM8之间的数据类型映射
   - 特殊类型可能需要手动调整

3. **性能问题**
   - 使用多线程提高迁移速度
   - 可以通过参数调整优化性能

## 贡献

欢迎提交Issue和Pull Request来帮助改进这个工具。

## 许可证

MIT License 