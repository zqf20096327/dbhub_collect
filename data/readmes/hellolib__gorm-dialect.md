
# gorm-dialect
Gorm v2 方言包
## 版本
v2-dm8 （gorm v2版本 达梦8 数据库方言包）
## 使用说明
1. 拉取代码
```go
go get -u github.com/hellolib/gorm-dialect/v2
```
2. 示例
```go
package main
import (
	"github.com/hellolib/gorm-dialect/v2/dm"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)
type Product struct {
	gorm.Model
	Code string
	Price uint
}
func main() {
	db, err := gorm.Open(dm.Open("dm://SYSDBA:*****@localhost:5236"),
		&gorm.Config{Logger: logger.Default.LogMode(logger.Info),})
	if err != nil {
		panic("failed to connect database")
	}
	// 迁移 schema
	db.AutoMigrate(&Product{})
	// Create
	db.Create(&Product{Code: "D42", Price: 100})
	// Read
	var product Product
	//此处加上会带上id和下一句拼接，查询语句为取一条delete_at为空的id，并把id作为条件加到后面语句
	//db.First(&product) // 根据整型主键查找
	db.First(&product, "\"code\" = ?", "D42") // 查找 code 字段值为 D42 的记录
	// Update - 将 product 的 price 更新为 200
	db.Model(&product).Update("price", 200)
	// Update - 更新多个字段
	db.Model(&product).Updates(Product{Price: 200, Code: "F42"}) // 仅更新非零值字段
	db.Model(&product).Updates(map[string]interface{}{"Price": 200, "Code": "F42"})
	// Delete - 删除 product
	db.Delete(&product,1)
}
```
