# About SQLiteUtils
一个简单的基于Android的Sqlite数据库的操作封装，它有如下的好处:

- 便捷地创建表和增添表字段
- 通过操作对象来insert或者update表记录
- 支持多种查询方式，支持分页查询
- 支持事务

# Quick Start:

1. 定义表对应的对象，对于基本类型，请使用对象类型来声明类成员，如int用Integer。以免在update的时候出现意想不到的情况。
```java
@Table(name="t_user")
public class UserModel {
	@Table.Column(name="user_id",type=Column.TYPE_INTEGER,isPrimaryKey=true)
	public Integer userId;
	
	@Table.Column(name="user_name",type=Column.TYPE_STRING,isNull=false)
	public String userName;
	
	@Table.Column(name="born_date",type=Column.TYPE_TIMESTAMP)
	public Date bornDate;
	
	@Table.Column(name="pictrue",type=Column.TYPE_BLOB)
	public byte[] pictrue;
	
	@Table.Column(name="is_login",type=Column.TYPE_BOOLEAN)
	public Boolean isLogin;
	
	@Table.Column(name="weight",type=Column.TYPE_DOUBLE)
	public Double weight;
}
```
2. 增删查改:
初始化对象:
```java
SQLiteDatabase db = context.openOrCreateDatabase("test.db", Context.MODE_PRIVATE, null);
DbSqlite dbSqlite = new DbSqlite(db);
IBaseDao<UserModel> userDAO = DaoFactory.createGenericDao(dbSqlite, UserModel.class);
```
创建Table:
```java
userDAO.createTable();
```
insert 一条记录：
```java
UserModel user = new UserModel();
user.userName = "darcy";
user.isLogin = true;
user.weight = 60.5;
user.bornDate = new Date();
byte[] picture = {0x1,0x2,0x3,0x4};
user.pictrue = picture;
userDAO.insert(user);
```
update 记录:
```java
UserModel user = new UserModel();
user.weight = 88.0;
userDAO.update(user, "user_name=?", "darcy");
```
查询结果:
```java
//单条结果查询
UserModel user = userDAO.queryFirstRecord("user_name=?", "darcy");

//一般查询
List<UserModel> userList = userDAO.query("user_name=? and weight > ?", "darcy" , "60");

//分页查询
PagingList<UserModel> pagingList = userDAO.pagingQuery(null, null, 1, 3);
```
事务支持:
```java
DBTransaction.transact(mDb, new DBTransaction.DBTransactionInterface() {
		@Override
		public void onTransact() {
			// to do 		
		}
};
```
更新表[只支持添加字段]:
```java
@Table(name="t_user" , version=2) //修改表版本
public class UserModel {
	//members above...
	
	//new columns
	
	@Table.Column(name="new_column_1",type=Column.TYPE_INTEGER)
	public Integer newColumn;
	
	@Table.Column(name="new_column_2",type=Column.TYPE_INTEGER)
	public Integer newColumn2;
}

userDAO.updateTable();
```
# License

   Copyright 2016 yedaxia

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
