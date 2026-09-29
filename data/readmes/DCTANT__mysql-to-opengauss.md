# MySQL全量传输OpenGauss工具
![封面](asset/banner.jpg)

本项目的功能为将MySQL中的全部数据传输到OpenGauss中。OpenGauss的库需要用户提前建好，本工具只提供建表和传输数据的功能。

## 前言
项目建立初衷为OpenGauss官方的MySQL迁移OpenGauss的工具无法正常使用，各种报错！原因是MySQL配置以及环境要求非常严格。一年前提的issue，至今没有解答，还不如我自己开发一套呢！

### 官方issue：

https://gitcode.com/opengauss/openGauss-migration-portal/issues/96

https://gitcode.com/opengauss/openGauss-migration-portal/issues/113

## 功能
### 表转换
将MySQL中的数据库表转换为OpenGauss数据库的表结构，支持OpenGauss A、B两种模式

### 数据传输
将MySQL中成功转换的表中的数据全量传输到OpenGauss中，支持OpenGauss A、B两种模式

### 生成报表
执行完成后会自动生成数据迁移的报表，可在result目录内查看。如果存在报错信息，则每个表都会输出对应的报错信息

### 附加功能
MySQL数据库间互相迁移，由于支持OpenGauss B模式（MySQL），也就导致了这个项目是支持MySQL间互相迁移的，只需要修改配置文件即可

## 运行环境
### 系统要求
目前仅在Linux系统完成测试，运行脚本只适合于Linux系统，Windows系统请下载源代码后直接运行

### 源数据库
目前我仅在MySQL 8.0.40中完成测试开发，建议使用MySQL8.x

### 目标数据库
目前我仅在OpenGauss 6.0.10中完成测试开发，建议使用OpenGauss6.x

### java环境
由于本项目全部使用java开发，因此需要java运行环境，建议jdk版本大于等于17

## 运行方式
* 如果auto-run为true，则启动项目自动就开始全量数据迁移工作
* 如果auto-run为false，则启动项目后，可通过接口调用全量数据迁移

## 项目优势
* 支持OpenGauss A模式（PostgreSQL）和B模式（MySQL），官方迁移工具只支持B模式（MySQL）
* 采用java编写，代码简单明了，功能清晰
* 安装包非常小
* 配置文件修改简洁明了
* 无需其他中间件，不需要使用zookeeper和kafka
* 没有乱七八糟花里胡哨的东西，我从来不会为了用而用，这里全部使用线程池干就完了
* 可选择自动运行还是选择接口调用再运行
* 支持配置需要迁移的表和过滤不需要迁移的表
* 执行完成后有报表输出，能够清晰查看数据迁移结果
* 全程自主可控
* 支持MySQL间数据迁移

## 使用方法
1. 下载发行版中的tar.gz包，并上传到Linux服务器中
2. 使用以下命令解压安装包
<code language="bash">
tar -zxvf mysql-to-opengauss-*.tar.gz
</code>
3. 进入解压后的目录，并进入config目录
4. 修改application-demo.yaml，修改其中的MySQL和OpenGauss的连接地址
5. 返回上一级，进入bin目录
6. 执行命令：
<code language="bash">
./start.sh
</code>
启动迁移项目
7. 如果application-demo.yaml中的auto-run为true，则项目会自动开始全量迁移
8. 如果application-demo.yaml中的auto-run为false，则项目启动后，可以通过接口调用全量数据迁移

## 接口信息
### 全量迁移，与auto-run执行的内容一致
curl --location --request POST '{IP地址}:8845/mto/fullConvert'

### 仅转换表
curl --location --request POST '{IP地址}:8845/mto/covertTables'

### 仅迁移数据
curl --location --request POST '{IP地址}:8845/mto/transferData'