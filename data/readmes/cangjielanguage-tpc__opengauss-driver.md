# opengauss-driver

#### 介绍
opengauss-driver是纯仓颉语言实现的[openGauss](https://opengauss.org/)和[PostgreSQL](https://www.postgresql.org/)数据库驱动。

#### 软件架构
[前后端通信协议模块](https://www.postgresql.org/docs/current/protocol.html): proto3

前后端连接管理模块: pgconn

驱动接口实现模块: driver

简单数据库连接池模块: sqlpool

#### 使用说明

先使用data目录里面的sql文件创建样例表

```cangjie
import opengauss.driver.*
import std.database.sql.*

func do_insert(db: Datasource): Unit {
    let cn = db.connect()
    let sql = 
        #"INSERT INTO "some_types" ("created_at","updated_at","deleted_at","source") VALUES ('2022-12-29 11:02:25.566','2022-12-29 11:02:25.566',NULL,'Dec 15 11:02:25') RETURNING "id""#
    try (st = cn.prepareStmt(sql)) {
        if (let Update(ur) = st.execute()) {
            logger.debug("${ur.rowCount}, ${ur.lastInsertId}")
        }
    } catch (e: Exception) {
        logger.error(e.message)
        e.printStackTrace()
    }
}

func do_query_single(db: Datasource): Unit {
    let cn = db.connect()
    let sql = "SELECT * FROM public.change_logs ORDER BY id ASC"
    try (st = cn.prepareStmt(sql)) {
        if (let Query(qr) = st.execute()) {
            while (qr.next()) {
                logger.debug(
                    "${qr.getString(0)} ${qr.getTime(1)} ${qr.getString(2)} ${qr.getString(3)} ${qr.getString(6)}")
            }
            qr.close()
        }
    } catch (e: Exception) {
        logger.debug("exception ${e.message}")
        e.printStackTrace()
    }
}
func test_og(): Unit {
    var url = "opengauss://gorm:pass@7.212.133.32:5432/loggable?sslmode=disable"
    let db = sqlpool.openDb("opengauss", url)
    let p = db.ping()
    println("ping opengauss OK.")
    do_insert(db)
    do_query_single(db)
}
func test_pg(): Unit {
    logger.level = LogLevel.DEBUG
    var url = "postgres://gorm:pass@127.0.0.1:5432/loggable?sslmode=disable"
    let db = sqlpool.openDb("postgres", url)
    let p = db.ping()
    println("ping postgres OK.")
    do_insert(db)
    do_query_single(db)
}
main() {
	test_og()
	test_pg()
}

```



#### 参与贡献

1.  Fork 本仓库
2.  新建 feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

