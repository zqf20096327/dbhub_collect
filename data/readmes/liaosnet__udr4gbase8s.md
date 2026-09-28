# UDR for GBase 8s
User define routine for GBase 8s Database Server  

## 编译 
编译环境需求：  
- GBase 8s CSDK  
- GCC编译环境  

按CSDK安装目录修改makefile  

执行编译：make  

## 在数据库中注册  
复制libudr4gbase8s.udr和udr_for_gbase8s_function.sql到数据库的安装目录下的udr目录下（`$GBASEDBTDIR/udr`）  
在需要库中注册udr函数：dbaccess -e 库名 udr_for_gbase8s_function.sql  

## 使用函数  
示例：select tabid, first_row(tabname), last_row(tabname) from systables;  

## 已实现函数列表  
|UDR函数名|对应udr中的函数|功能|
|:---|:---|:---|
|udr_first_row_init|udr_first_row_init|聚集函数first_row/last_row的init函数|
|udr_first_row_iter|udr_first_row_iter|聚集函数first_row的iter函数|
|udr_first_row_combine|udr_first_row_combine|聚集函数first_row/last_row的combine函数|
|first_row|无|聚集函数，由init,iter和combine组成|
|udr_last_row_iter|udr_last_row_iter|聚集函数last_row的iter函数|
|last_row|无|聚集函数，由init,iter和combine组成|
|udr_cast_bool_integer|udr_cast_bool_integer|cast转换函数boolean转int|
|udr_cast_integer_bool|udr_cast_integer_bool|cast转换函数int转boolean|
