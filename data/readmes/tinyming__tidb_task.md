# 描述
tidb小作业
# 程序执行
## 程序入口
  service下的Tidb 的main函数
## 程序输入
n 一个整数，即模拟n个TiDb客户端。每个client读取的文件以sql_text_n.txt的方式命名。比如n输入为3则需准备sql_text_1.txt、sql_text_2.txt、
sql_text_3.txt 文件需放在webapp目录下。
# 解题思路
## 模拟多个client
  通过多线程的方式模拟多个client，每个client对应一个线程，读取相应的内容。通过Future来实现获取所有的读取结果。读取文件通过ReadSqlTask类实现。
## 获取所有的执行顺序case
  通过将所有的sql语句进行全排列，然后删除打乱了原有顺序的case（运行过程中有打印所有的case）。主要逻辑都在TiDb里。
  
## 执行sql
  通过mybaits链接数据库，然后执行对应的语句。
  
