# dm

### 介绍
``` 
go get github.com/OpenOnHere/dameng-golang
```  
达梦数据库官方Go驱动,本项目和官方驱动版本同步,方便go mod 使用.  
达梦官方文档:https://eco.dameng.com/docs/zh-cn/app-dev/go-go.html    
资源下载:https://eco.dameng.com/download/    
达梦官方Go驱动包:https://package.dameng.com/eco/adapter/resource/go/dm-go-driver.zip  
达梦官方论坛(提交bug):https://eco.dameng.com/community/question  

### Xorm
[Xorm](https://xorm.io/) 是一个Go语言的对象关系映射（ORM）库，它提供了一种简单而强大的方式来操作数据库。Xorm 可支持当前驱动
Xorm-adapter: https://github.com/OpenOnHere/xorm-adapter

### DSN  
dm://userName:password@127.0.0.1:5236?schema=DBName  
用户名(userName)默认就是数据库的名称,达梦用户模式和数据库名称是对应的,也可以通过schema参数指定数据库  
建议达梦使用UTF-8字符编码,不区分大小写,建表语句的字段名不要带""双引号       
密码中包含特殊字符时,密码使用url.PathEscape进行Escape处理,并在DSN中加入&escapeProcess=true   参见:https://eco.dameng.com/community/question/d152258b30bd0fc030d15e6a4afd5fc2  

### bug
- 达梦开启等保参数 COMM_ENCRYPT_NAME = AES128_ECB,导致连接异常