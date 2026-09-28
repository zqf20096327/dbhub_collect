
# SimpleDB: a minimalist Key Value store written in Java

This project was done following the guide [build your own database](https://build-your-own.org/database/). The result is the equivalent of Part I of that guide: a simple append-only Key Value Store which uses a B+ Tree and a Free List.

Translating the ideas from Go to Java was a challenge and probably some performance was lost on the way, nevertheless this project's goal was to have fun and as a consequence learning as well.

Special thanks to [abedmohammed](https://github.com/abedmohammed/goDB) whose project was also a good reference in moments where the previous guide was not clear enough.

### Requirements:

- Java 17+
- Maven
- UNIX based OS

### Example

```java
    Store store = Store.getInstance("mydatabase");
    
    byte[] key = NodeOps.stringToBytes("some key");
    byte[] value = NodeOps.stringToBytes("some value");
    
    store.set(key, value);
    
    byte[] retrieved = store.get(key);
    
    System.out.write(retrieved);
    System.out.println();
    
    store.delete(key);
```

### Performance

See __massReadPerformanceTest__ in __KvStoreTest.java__
```
Read 10000 key-value pairs in 432 ms
Average time per read: 0.0432 ms
```
See __massInsertionPerformanceTest__
```
Inserted 10000 key-value pairs in 9529 ms
Average time per insertion: 0.9529 ms
```

### Tests

```bash
mvn clean verify
```

### TODO

- Optimize write speed
- Concurrency control
