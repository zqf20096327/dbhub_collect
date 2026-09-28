# 达梦 gorm-dm-driver（官方源码：2025/05/13）

### 达梦数据库 gorm方言包

> 使用方法同gorm官方支持的mysql、postgres等一致
>
### go get
```shell
go get github.com/jasonlabz/gorm-dm-driver@master
```

### DSN格式:
```shell
dm://user:password@host:port?schema=SYSDBA[&propName2=propValue2]…
```

### 具体用法示例
可参考： [代码示例: https://github.com/jasonlabz/dbutil/blob/master/dbx/db.go](https://github.com/jasonlabz/dbutil/blob/master/dbx/db.go)
```go
package main

import (
	"gorm.io/gorm"
	dm "github.com/jasonlabz/gorm-dm-driver"
)

func main() {
	dialect := dm.Open("dm://user:password@host:port?schema=SYSDBA[&propName2=propValue2]…")

	db, err := gorm.Open(dialect)
	if err != nil {
		return err
	}

	sqlDB, err := db.DB()
	if err != nil {
		return err
	}
	//sqlDB.SetMaxOpenConns(config.MaxOpenConn)
	//sqlDB.SetMaxIdleConns(config.MaxIdleConn)
	//sqlDB.SetConnMaxLifetime(config.ConnMaxLifeTime)
	//dbWrapper := &DBWrapper{
	//	DB:     db,
	//	Config: config,
	//}
	//dbMap.Store(config.DBName, dbWrapper)
	//return nil
}

```
