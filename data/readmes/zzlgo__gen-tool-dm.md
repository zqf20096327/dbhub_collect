# gen-tool-dm

gentool支持达梦数据库，基于gentool 0.3.27版本进行扩展，将gentool改为gen-tool-dm即可，其余保持不变

## 安装

```shell
 go install github.com/zzlgo/gen-tool-dm@latest
```

## 使用达梦参考

gen-tool-dm -db=dm -dsn "dm://username:password@host:port?schema=database" \
-outPath="./dao" \
-tables="tableName" \
-modelPkgName model

## 测试表

```sql
CREATE TABLE IF NOT EXISTS "USER"
(
    "ID"         BIGINT IDENTITY(1, 1) NOT NULL PRIMARY KEY,
    "NAME"       VARCHAR(100) NOT NULL DEFAULT '',
    "CREATED_AT" TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "UPDATED_AT" TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## 生成的model

```go
package model

import (
	"time"
)

// User mapped from table <USER>
type User struct {
	ID        int64     `gorm:"column:ID;type:BIGINT;primaryKey" json:"id"`
	Name      string    `gorm:"column:NAME;type:VARCHAR;not null" json:"name"`
	CreatedAt time.Time `gorm:"column:CREATED_AT;type:TIMESTAMP;not null;default:CURRENT_TIMESTAMP" json:"created_at"`
	UpdatedAt time.Time `gorm:"column:UPDATED_AT;type:TIMESTAMP;not null;default:CURRENT_TIMESTAMP" json:"updated_at"`
}

```



