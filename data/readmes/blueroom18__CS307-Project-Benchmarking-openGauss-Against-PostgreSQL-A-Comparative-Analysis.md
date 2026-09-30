# Benchmarking-openGauss-Against-PostgreSQL-A-Comparative-Analysis
sql-based database comparisons between OpenGuass and PostgreSql

SqlGenerator is a java programme to generate multiple insert orders to give datas;
SqlGenerator is a java programme to generate multiple transanctions to give datas;
test_1 ~ 4 corresponds with the 4 property-tests in my .md article.
You can find more in .md and the article is in Chinese, the English version will be updated soon.

## You can replicate my experiment and verify the OpenGauss database by following these steps.
First you could use dockers to set the environment for this two databases(you could refer to the openGauseGuideline.pdf) and use Datagrip to make connections. After doing that you could open two console for two databases and make some tests as below.  
1.You could use SqlGenerators to generate multiply insertions(you could adjust columns and rows in this Java programme)  

```
public static void main(String[] args) {
        // Input settings here
        long m = 50000;  // row setting
        long n = 2;  // column setting
        String[] columnNames = {"id", "name", "age"};
        String[] columnTypes = {"int", "varchar", "long"};
```

2.Then you could do these insertions in the console seperately to see whether the running time comparison corresponds with my work.  
3. Ok, so now you have a form with big amount of datas. You could try UPDATE,SELECT,SUM,AVERAGE and so on, comparing your result with mine. P.A. you could add EXPLAIN ANALYSE at the beginning of these simple DML to see the time for different steps and the momery occupaid.  
4. Also, you could open several consoles to test the locks for this two databases. The detailed process is in the .md file and you could use the sql in it.  
5. Then you could try to use SqlGenerator to generate multiple transanctions, you could also change the numbers or the content of the transactions to test more situations. Also add EXPLAIN ANALYSE when testing to see the detailed information.  
6. You could try to import the datas(like .csv files) in to test whether in this way OpenGuass do better than PostgreSQL.  
7. The last step in my work is about multi-join tables'test. You could find the source sql code in the fourth sql file and you could compare the result with mine. Maybe the complexity in my work is not that persuative, you could try more in this way.  

### Some words
The creator of this work is a greenhand in this field and maybe do a lot of things improperly, please be careful if you'd like to test in my way. And more detailed information is in my .md file.
