

### 基于SpringBoot + Vue高校学生心理健康调查系统.

大学生心理健康干预、心理咨询预约系统、心理亚健康监测。

> 管理员: 文章管理、系统公告、试卷管理、贴子管理、答题记录、贴子回复、学生管理、教师管理、贴子模块

> 教师: 个人信息、学生信息、学生答题、试卷管理

> 学生: 个人信息、我的贴子、我的回复、答题记录、心灵文章、试卷答题

##### 基础管理模块
###### 学生/教师管理： 维护全校师生基础档案，支持账号权限分配与信息导出。

###### 个人信息： 提供用户信息维护界面，支持头像、联系方式及密码修改。

###### 系统公告： 管理员发布政策文件或活动通知，确保关键信息直达师生。

##### 心理测评模块
###### 试卷管理： 教师与管理员设计、编辑心理量表，灵活设置测评题目。

###### 试卷答题： 学生在线参与心理自测，系统实时记录反馈，提供便捷终端。

###### 学生答题/记录： 自动汇总测评结果，方便教师调阅分析，建立动态档案。

##### 互动交流模块
###### 贴子管理/模块： 管理员统筹社区版块，审核违规内容，营造健康讨论氛围。

###### 我的贴子/回复： 学生自由表达情感、互动互助，记录个人心路历程与交流。

###### 贴子回复（管理）： 及时解答学生困惑，通过评论引导建立正向的心理反馈。

##### 内容服务模块
###### 文章管理： 管理员上传心理科普、减压技巧等推文，丰富平台教育资源。

###### 心灵文章： 学生阅读专业心理文章，学习自救知识，提升心理健康素养。

#### 安装环境

JAVA 环境 

Node.js环境 [https://nodejs.org/en/] 选择14.17

Yarn 打开cmd， 输入npm install -g yarn !!!必须安装完毕nodejs

Mysql 数据库 [https://blog.csdn.net/qq_40303031/article/details/88935262] 一定要把账户和密码记住

redis

Idea 编译器 [https://blog.csdn.net/weixin_44505194/article/details/104452880]

WebStorm OR VScode 编译器 [https://www.jianshu.com/p/d63b5bae9dff]

#### 采用技术及功能

后端：SpringBoot、MybatisPlus、MySQL、Redis、
前端：Vue、Apex、Antd、Axios

平台前端：vue(框架) + vuex(全局缓存) + rue-router(路由) + axios(请求插件) + apex(图表)  + antd-ui(ui组件)

平台后台：springboot(框架) + redis(缓存中间件) + shiro(权限中间件) + mybatisplus(orm) + restful风格接口 + mysql(数据库)

开发环境：windows10 or windows7 ， vscode or webstorm ， idea + lambok

#### 前台启动方式
安装所需文件 yarn install 
运行 yarn run dev

#### 后端启动方式

1.首先启动redis，进入redis目录终端。输入redis-server回车
2.导入sql文件，修改数据库与redis连接配置
3.idea中启动后端项目

#### 默认后台账户密码
[管理员]
admin
1234qwer

[学生]
fank
1234qwer

[导师]
fank
1234qwer

#### 项目截图

|  |  |
|---------------------|---------------------|
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666140685.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712718216285.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712718196396.png) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666121087.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712718179757.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666108598.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666210751.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666047227.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666199567.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666032850.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666189961.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666016011.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666174255.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666003576.jpg) |
|![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712666156188.jpg) | ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/1712665989291.jpg) |
| ![](https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/work/936e9baf53eb9a217af4f89c616dc19.png) |


#### 演示视频

暂无

#### 获取方式

Email: fan1ke2ke@gmail.com

WeChat: `Storm_Berserker`

`附带部署与讲解服务，因为要恰饭资源非免费，伸手党勿扰，谢谢理解😭`

> 1.项目纯原创，不做二手贩子 2.一次购买终身有效 3.项目讲解持续到答辩结束 4.非常负责的答辩指导 5.**黑奴价格**

> 项目部署调试不好包退！功能逻辑没讲明白包退！

#### 其它资源

[2025年-答辩顺利通过-客户评价🍜](https://berserker287.github.io/2025/06/18/2025%E5%B9%B4%E7%AD%94%E8%BE%A9%E9%A1%BA%E5%88%A9%E9%80%9A%E8%BF%87/)

[2024年-答辩顺利通过-客户评价👻](https://berserker287.github.io/2024/06/06/2024%E5%B9%B4%E7%AD%94%E8%BE%A9%E9%A1%BA%E5%88%A9%E9%80%9A%E8%BF%87/)

[2023年-答辩顺利通过-客户评价🐢](https://berserker287.github.io/2023/06/14/2023%E5%B9%B4%E7%AD%94%E8%BE%A9%E9%A1%BA%E5%88%A9%E9%80%9A%E8%BF%87/)

[2022年-答辩通过率100%-客户评价🐣](https://berserker287.github.io/2022/05/25/%E9%A1%B9%E7%9B%AE%E4%BA%A4%E6%98%93%E8%AE%B0%E5%BD%95/)

[毕业答辩导师提问的高频问题](https://berserker287.github.io/2023/06/13/%E6%AF%95%E4%B8%9A%E7%AD%94%E8%BE%A9%E5%AF%BC%E5%B8%88%E6%8F%90%E9%97%AE%E7%9A%84%E9%AB%98%E9%A2%91%E9%97%AE%E9%A2%98/)

[50个高频答辩问题-技术篇](https://berserker287.github.io/2023/06/13/50%E4%B8%AA%E9%AB%98%E9%A2%91%E7%AD%94%E8%BE%A9%E9%97%AE%E9%A2%98-%E6%8A%80%E6%9C%AF%E7%AF%87/)

[计算机毕设答辩时都会问到哪些问题？](https://www.zhihu.com/question/31020988)

[计算机专业毕业答辩小tips](https://zhuanlan.zhihu.com/p/145911029)


#### 接JAVAWEB毕设，纯原创，价格公道，诚信第一

`网站建设、小程序、H5、APP、各种系统 选题+开题报告+任务书+程序定制+安装调试+项目讲解+论文+答辩PPT`

More info: [悲伤的橘子树](https://berserker287.github.io/)

<p><img align="center" src="https://fank-bucket-oss.oss-cn-beijing.aliyuncs.com/img/%E5%90%88%E4%BD%9C%E7%89%A9%E6%96%99%E6%A0%B7%E5%BC%8F%20(3).png" alt="fankekeke" /></p>

