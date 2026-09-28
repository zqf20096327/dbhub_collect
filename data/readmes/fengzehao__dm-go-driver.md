# DM Go Driver

本项目是达梦数据库 (Dameng Database) 的 Go 语言驱动程序,支持通过远程仓库直接引入。

## ⚙️ 安装

在你的 Go 项目根目录下运行以下命令即可添加依赖：

```bash
go get github.com/fengzehao/dm-go-driver@latest
```

## 🚀 快速开始
```go
package main

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/fengzehao/dm-go-driver"
)

func main() {
    // 格式: dm://用户名:密码@主机:端口
	// 注意: 达梦默认端口通常是 5236，默认用户名密码通常是 SYSDBA/SYSDBA
	db, err := sql.Open("dm", "dm://SYSDBA:SYSDBA001@127.0.0.1:5236")
	if err != nil {
		log.Fatal(err)
	}
	if err = db.Ping(); err != nil {
		log.Fatal(err)
	}
	var id int
    querySql := "select id from tuser test_user where name='test'"
	err = db.QueryRow(querySql).Scan(&id)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("查询结果 -> ID: %d", id)
    // 记得关闭连接
	_ = db.Close()
}
```