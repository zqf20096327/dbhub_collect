DataEase v2 数据源插件开发文档
插件可提高系统拓展性。
本文介绍如何开发一个数据源插件。
注意：开发插件需要使用Java，Vue相关技术。

一、插件接口
从github中获取dataease工程，并在本地安装。
1.获取插件接口
Github地址：https://github.com/dataease/dataease
下载源码后，切换到所需分支

2.本地安装插件接口
进入项目的根目录，执行mvn clean install，等待命令执行成功即可。

二、插件demo
以hive插件为例
1.新建工程，并创建3个module。开发时，在dataease工程同级目录下创建extensions目录，将extensions-ds-hive插件工程放入extensions中，便于调试

hive-backend ：后端代码
hive-frontend ：前端代码，开发调试使用
hive-frontend-package ：前端打包使用，注意如果前端代码用到主工程中的组件，需要将组件复制到插件中
2.hive-backend介绍
a.插件后端需继承DataEaseDatasourcePlugin类，并实现其中接口，具体接口的作用可在代码注释中找到。

b.在resources/plugin目录下，提供插件的json描述文件和插件logo的svg。注意命名规范，.json与.svg的文件名与moduleName一致。

json描述文件说明如下：
{  "name": "Apache Hive数据源插件",  "flag": "ds",// 固定ds  "developer": "fit2cloud",  "moduleName": "extensions-ds-hive",  "version": "v2.9.0",  "requireVersion": "v2.9.0",  "config": {    "driverPath": "/opt/dataease2.0/drivers/plugin/hiveDriver",// 驱动路径    "name": "Apache Hive",    "category": "DL",// 分类 ['OLTP', 'OLAP', 'DL', 'OTHER', 'LOCAL']    "extraParams": "",    "type": "hive",    "flag": 4,// 数据库标识，与DataSourceType.java和其余插件不同即可    "prefix": "`",// sql关键字前缀    "suffix": "`",// sql关键字后缀    "staticMap": {      "index": "ZXh0ZW5zaW9ucy1kcy1oaXZlL2NvbXBvbmVudC9pbmRleA=="    }  }}
c.驱动目录
将插件用到的驱动放到resources目录下。

3.hive-frontend和hive-frontend-package介绍
a.前端代码在src/component/index.vue中，打包时会复制到hive-frontend-package里。

b.如果index.vue中有用到主工程的组件，需要将组件复制到hive-frontend-package对应的目录下。


c.vite.config.ts和rollup.js中，修改相应的配置信息，如下图所示，包括但不仅限于红框内的部分，其余配置有需要也可修改。

d.index.vue中的代码，即数据源界面的配置信息，按需编写即可。



四、打包安装
注意：打包时前端pom.xml中一些指令。

	开发完成后，执行mvn clean package打成jar包，打开dataease的插件管理页面，上传插件即可。注意：更新插件需要重启dataease服务。

