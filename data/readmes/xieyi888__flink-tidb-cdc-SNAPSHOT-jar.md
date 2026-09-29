# flink-tidb-cdc-SNAPSHOT-jar

pom:
```java
        <dependency>
            <groupId>com.ververica</groupId>
            <artifactId>flink-sql-connector-tidb-cdc</artifactId>
            <version>2.2.0-yd-jira7134-20220512</version>
        </dependency>
        
        
        <dependency>
            <groupId>com.ververica</groupId>
            <artifactId>flink-connector-tidb-cdc</artifactId>
            <!-- The dependency is available only for stable releases, SNAPSHOT dependency need build by yourself. -->
            <version>2.2.0-yd-jira7134-20220512</version>
        </dependency>
```

flink-connector-tidb-cdc jar: https://github.com/xieyi888/flink-tidb-cdc-SNAPSHOT-jar/blob/master/flink-connector-tidb-cdc-2.2.0-yd-jira7134-20220512.jar

flink-sql-connector-tidb-cdc jar: https://github.com/xieyi888/flink-tidb-cdc-SNAPSHOT-jar/blob/master/flink-sql-connector-tidb-cdc-2.2.0-yd-jira7134-20220512.jar

只有flink-sql-connector-tidb-cdc jar中打包进了修改后的org.tikv.common.operation.iterator.ScanIterator. 依赖仅添加flink-connector-tidb-cdc 应该不行，需要两项依赖都添加
