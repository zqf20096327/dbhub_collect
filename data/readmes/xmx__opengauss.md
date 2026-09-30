# openGauss

[![Go Version](https://img.shields.io/badge/Go-%3E%3D1.18-blue)](https://go.dev/)
[![License](https://img.shields.io/badge/License-BSD%203--Clause-green.svg)](LICENSE)

> ⚠️ **重要提示**：本驱动仅支持 **openGauss** 数据库，**不支持 GaussDB**。两者虽然同属华为生态，但底层协议和驱动并不兼容，使用前请务必确认你的数据库类型为 openGauss，否则将无法正常连接。

## 安装

```bash
go get github.com/xmx/opengauss
```

## 快速开始

```go
package main

import (
    "gorm.io/gorm"
    "github.com/xmx/opengauss"
)

type User struct {
	ID   int64  `json:"id"   gorm:"column:id;primaryKey"`
	Name string `json:"name" gorm:"column:name;size:128;comment:用户名"`
	Age  int    `json:"age"  gorm:"column:age;comment:年龄"`
}

func (User) TableName() string {
	return "user"
}

func main() {
    // 打开数据库连接
    db, err := gorm.Open(opengauss.Open("host=127.0.0.1 port=5432 user=dbuser password=secret dbname=mydb sslmode=disable"), &gorm.Config{})
    if err != nil {
        panic(err)
    }

    // 自动迁移表结构
    db.AutoMigrate(&User{})

    // CRUD 操作
    db.Create(&User{Name: "张三", Age: 30})
}
```
