# 达梦数据库的文件操作

使用DM8+Python

此文件是测试文件，没有UI界面

基本思路：将文件存储为二进制数据（BLOB）

## 数据库准备

### 创建一个名为`TEST0623`的数据库

可以使用自己的数据库，方法是修改`sql_query`

```python
sql_query = "INSERT INTO \"TEST0623\".\"files\" (filename, filedata) VALUES (?, ?)"
```





### 创建存放文件(二进制)的表

```sql
CREATE TABLE "TEST0623"."files" (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    -- BLOB（Binary Large Object）是一种用于存储大量二进制数据的数据库列类型。BLOB 类型通常用于存储各种类型的文件和数据，这些数据可能包括图像、音频、视频、文档等。由于 BLOB 可以处理大量数据，它适合存储可能非常大的二进制数据块。
    filedata BLOB,
    -- upload_time: 这是列的名称，用于存储文件的上传时间。
	-- TIMESTAMP: 这是列的数据类型，表示此列将存储时间戳。时间戳通常包括日期和时间。
	-- DEFAULT CURRENT_TIMESTAMP: 这是一个默认值约束，表示当插入新记录时，如果没有为 upload_time 列指定值，该列将自动使用当前的时间戳。
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 

### 配置自己的数据库接口

```python
connection = dmPython.connect(user='你的用户名', password='密码', server='localhost',
                        port=5236, autoCommit=True)
```



## 附录

### 软件包

dmPython为python提供连接达梦数据库的接口

```python
pip install dmPython
```



### open()函数

在 Python 中，`open()` 函数的参数可以是文件名或文件路径，这取决于文件的位置：

1. **文件名**：

   - 如果文件位于当前工作目录中，只需提供文件名。

   - 例如，如果文件 

     ```python
     example.pdf
     ```

      位于当前工作目录中，可以这样打开：

     ```python
     python复制代码with open('example.pdf', 'rb') as file:
         binary_data = file.read()
     ```

2. **文件路径**：

   - 如果文件不在当前工作目录中，需要提供文件的路径。这可以是相对路径或绝对路径。

   - 相对路径是相对于当前工作目录的路径，例如，如果文件在当前目录的子目录 

     ```python
     docs
     ```

      中，可以这样打开：

     ```python
     python复制代码with open('docs/example.pdf', 'rb') as file:
         binary_data = file.read()
     ```

