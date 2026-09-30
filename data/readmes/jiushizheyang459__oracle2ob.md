# Readme

* 本软件支持将Oracle数据库脚本转换为Oceanbase数据库脚本，目前仅支持Oceanbase Oracle模式，其他模式以及数据库后续支持
* 支持日志输出，若转换失败会显示在日志里并提示原因

### 使用方法

1.在oracle2ob.exe同级目录新建一个input文件夹

2.将需要转换的sql放在input文件夹里

3.打开oracle2ob.exe

4.转换完成后会生成output文件夹和log文件夹

5.转换完成后的sql会输出在output文件夹

6.查看log，看是否有转换失败的sql