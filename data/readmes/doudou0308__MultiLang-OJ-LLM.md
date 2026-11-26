# MultiLang OJ

面向本机开发与学习的编程评测工作台。支持 Java、C 和 C++，可编辑题目、配置执行规则和用例、运行自测、提交评测并查看历史。

## 本地启动

需要 JDK 17、Maven 3.6+、MySQL 8，以及 PATH 上的 GCC 和 G++。MySQL 中先建库：

```sql
CREATE DATABASE local_judge CHARACTER SET utf8mb4;
```

给本机数据库账号授予这个库的读写和建表权限。PowerShell 示例：

```powershell
$env:OJ_DB_USER = 'local_judge'
# MySQL 账号有密码时，在当前终端输入：
$env:OJ_DB_PASSWORD = Read-Host -MaskInput 'MySQL 密码'
mvn verify
java -jar target/local-judge-2.0.0-SNAPSHOT.jar
```

浏览器打开 <http://127.0.0.1:8080>。使用 `OJ_PORT` 可更换端口。程序会自动建表并在空库安装一道练习题。设置 `OJ_SEED_SAMPLE=false` 可从空题库启动。

| 变量 | 默认值 | 用途 |
| --- | --- | --- |
| `OJ_DB_URL` | `jdbc:mysql://127.0.0.1:3306/local_judge` | 数据库连接 |
| `OJ_DB_USER` | `local_judge` | 数据库账号 |
| `OJ_DB_PASSWORD` | 空 | 数据库密码 |
| `OJ_JAVAC` / `OJ_JAVA` | `javac` / `java` | Java 17 工具链 |
| `OJ_CC` / `OJ_CXX` | `gcc` / `g++` | C17 / C++17 工具链 |

Windows 可以把编译工具链目录加入 PATH，或把变量设为具体的可执行文件绝对路径。Java 代码入口为 `public class Main`。

## 数据和接口

- 题面、执行规则和有序用例分别存储。示例可公开展示，隐藏用例只有本机题目管理入口可见。
- 提交只编译一次，每个用例有独立工作目录，按用例记录结果。一次评测同时只占一个执行槽。自测结果无需写入数据库。
- 核心入口为 `GET /api/v2/exercises`、`POST /api/v2/exercises/{slug}/trials`、`POST /api/v2/exercises/{slug}/attempts` 和 `GET /api/v2/attempts`。题目创建、编辑和归档位于 `/api/v2/authoring/exercises`。
- 使用新库启动。现有数据库、历史账号和提交无需删除。要带入已有题目，可在题目管理页录入自己有权使用的题面、独立用例和执行规则。

## 运行边界

这是单用户本机工具。编译后的代码以当前操作系统用户身份执行，临时目录、时间和输出上限不能代替沙箱。只运行可信代码，保持服务监听回环地址。多个本机用户不能隔离题目和提交。

## 验证

`mvn verify` 运行判题规则及输入边界测试。服务启动并安装示例后，`python tools/smoke.py` 检查三种语言、自测、典型失败判定和提交历史。脚本会创建并归档一条验证用题目，并保存数条示例提交。请只对本地开发或测试库运行。
