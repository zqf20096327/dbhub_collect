#####  一、工具运行说明(执行结果见tidb-trx-test/sql/tidbtrxtest.log)
 
- 编译说明
> mvn package 

- 部署说明:
> 直接取编译好的jar包按运行说明执行即可   
> 位置: tidb-trx-test/target/tidb-trx-test-1.0.jar 

- 配置说明:
> src/main/resources/tidb-datasource.properties 
> 配置tidb数据库 url user password

- 运行说明:  
> 入参为文件名,可以两个或两个以上  
> nohup java -jar tidb-trx-test.jar $1 $2 .. > tidbtrxtest.log &  
> 样例:    
nohup java -jar tidb-trx-test-1.0.jar /Users/yuxiuzhen/IdeaProjects/ALL_IMS/tidb-trx-test/sql/sql1 /Users/yuxiuzhen/IdeaProjects/ALL_IMS/tidb-trx-test/sql/sql2 > tidbtrxtest.log &


#####  二、实现思路
> 1. 考虑到需要每个事务文件中的sql的执行顺序是确定的，所以把每个事务文件里的一个sql都抽象成相同的元素(下面实现中是一个文件用一个数字表示的)   
> 2. 每个事务文件抽象成一个元素相同的数组,长度为N+1,+1表示commit语句(如题中sql1文件表示为[0,0,0],sql2文件表示为[1,1])  
> 3. 将两个或者多个事务文件的sql组成一个数组(如题中则组合之后为[0,0,0,1,1])  
> 4. 将3中组合的数组进行全排序,实现中用了回溯+树层上去重,减少回溯次数(如题中因为多了commit执行的排序,所以最终的执行情况不止3种,具体见sql/tidbtrxtest.log的执行结果)  
> 5. 按上面的排列结果,一次执行CASE,如[0,0,0,1,1]的case,则建立两个客户端,按0和1出现的顺序分别按行读取sql1和sql2中的sql
> 6. 异常情况  
          - 如果更新条件一致会产生block,测试时的tidb默认60s会返回lock wait锁超时的错误),捕获异常继续执行下一个case   



#####  三、暂未完全实现的地方
> - 如果文件存在相同条件的更新SQL,会产生锁block等待, 超时会执行失败,目前的处理是捕捉异常,判定当前CASE执行失败,继续下一个CASE执行;
> - 程序未判断内存溢出的情况。
> - 文件中空行的情况未实现过滤



#####  四、题目：TiDB SQL 事务测试框架  
>描述：在测试 TiDB 事务时，对指定的两个事务，需要穷举两个客户端按不同的顺序执行 事务中的 SQL。   
例如给定两个事务，分别保存在 sql1 和 sql2 文件中。   
sql1 文件:   
    update X set a=5 where id=1;  
    update X set a=6 where id=2;   
sql2 文件:  
    update X set a=8 where id=8;   
对这个 case，穷举可能的 SQL 执行顺序，有以下三种情况：   
情况 1：   
    client1：update X set a=5 where id=1;   
    client1：update X set a=6 where id=2;   
    client2：update X set a=8 where id=8;   
情况 2：   
    client1：update X set a=5 where id=1;  
    client2：update X set a=8 where id=8;   
    client1：update X set a=6 where id=2;   
情况 3：   
    client2：update X set a=8 where id=8;  
    client1：update X set a=5 where id=1;   
    client1：update X set a=6 where id=2;   
要求：   
    1、写代码根据两个 sql 文件生成事务的 N 种 SQL 执行顺序组合（ 可以假设文件中一行 是一个 sql ）   
    2、写一个测试程序，能模拟两个客户端执行这 N 种组合（不用做结果校验）。   
    3、可以跑在 TiDB 上。  