# 伙伴匹配系统

| Author | zicai |
| :----: | :---: |

域名：http://www.zicai.site

后端 Swagger 接口文档地址：http://localhost:9090/api/doc.html

> 注意：需要自定义的环境我都做了 todo 标记，运行项目之前先将配置项修改为自己的
>

## 简述

​	本项目名为伙伴匹配系统，一个移动端 H5 网页，实现了以下功能，用于帮助用户匹配与自己相似的用户，一起学习、竞赛，共同进步。

- 用户可以设置自己账号的标签，可以根据自己的标签匹配与自己最相似的用户、根据标签搜索用户，找到志同道合的伙伴。
- 用户能够组队，创建自己的队伍、查找队伍，找到一起参加竞赛的伙伴，告别孤军奋战。
- 用户还可以关注其他用户，与其他用户用户私聊。



## 效果展示

![伙伴匹配1](imgs/伙伴匹配1.png)

![伙伴匹配2](imgs/伙伴匹配2.png)

![伙伴匹配3](imgs/伙伴匹配3.png)

![伙伴匹配4](imgs/伙伴匹配4.png)

![伙伴匹配5](imgs/伙伴匹配5.png)

![伙伴匹配6](imgs/伙伴匹配6.png)

![伙伴匹配7](imgs/伙伴匹配7.png)

![伙伴匹配8](imgs/伙伴匹配8.png)

![伙伴匹配9](imgs/伙伴匹配9.png)

![伙伴匹配10](imgs/伙伴匹配10.png)

![伙伴匹配11](imgs/伙伴匹配11.png)

![伙伴匹配12](imgs/伙伴匹配12.png)

![伙伴匹配13](imgs/伙伴匹配3.png)

![伙伴匹配14](imgs/伙伴匹配14.png)

![伙伴匹配15](imgs/伙伴匹配15.png)



## 技术选型

​	前后端分离架构

开发平台：WebStorm 2023 + IntelliJ IDEA 2023 + Navicat Premium16

**前端**

- JavaScript 脚本语言
- Vue3 前端框架
- VantUI 移动端 H5 组件库
- Vite 2 打包工具
- Nginx部署

**后端**

- Java 语言
- Spring 框架
- SpringMVC 表现层框架
- MyBatis 持久层框架
- MyBatis-Plus 持久层框架
- WebSocket 通信协议
- SpringBoot 框架整合第三方技术简化开发
- MySQL 数据库
- Redis 数据库

**部署**

- Ubuntu18 腾讯云 2核4G 服务器
- MySQL 8.0 腾讯云 1核1G 数据库
- Redis 5.0 腾讯云 256M 数据库



## 数据库表设计

​	用于存储用户数据

### 1. 用户表 `user`

**字段**

1. id 主键
2. username 用户昵称
3. userAccount 账号
4. avatarUrl 用户头像url地址
5. gender 性别 0-男 1-女
6. userPassword 密码
7. phone 电话
8. email 邮箱
9. userStatus 状态 0-正常
10. createTime 创建时间
11. updateTime 修改时间
12. isDelete 逻辑删除 1-已删除
13. userRole 用户角色
14. planetCode 星球编号
15. tags 用户标签
16. profile 个人简介



**建表语句**

```sql
create table user
(
    username     varchar(256)                       null comment '用户昵称',
    id           bigint auto_increment comment 'id'
        primary key,
    userAccount  varchar(256)                       null comment '账号',
    avatarUrl    varchar(1024)                      null comment '用户头像',
    gender       tinyint                            null comment '性别',
    userPassword varchar(512)                       not null comment '密码',
    phone        varchar(128)                       null comment '电话',
    email        varchar(512)                       null comment '邮箱',
    userStatus   int      default 0                 not null comment '状态 0 - 正常',
    createTime   datetime default CURRENT_TIMESTAMP null comment '创建时间',
    updateTime   datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    isDelete     tinyint  default 0                 not null comment '是否删除',
    userRole     int      default 0                 not null comment '用户角色 0 - 普通用户 1 - 管理员',
    planetCode   varchar(512)                       not null comment '星球编号',
    tags         varchar(1024)                      null comment '标签 json 列表',
    profile      varchar(512)                       null comment '个人简介'
)
    comment '用户';
```



### 2. 标签表 `tag`

​	用于存储标签数据

**字段**

1. id 主键
2. tagName 标签名称
3. userId 创建的用户id 逻辑外键
4. parentId 父标签id
5. isParent 是否为父标签
6. createTime 创建时间
7. updateTime 更新时间
8. isDelete 逻辑删除 1-已删除



**建表语句**

```sql
create table user_tag
(
    id         bigint auto_increment comment 'id'
        primary key,
    tagName    varchar(256)                       null comment '标签名称',
    userId     bigint                             null comment '用户 id',
    parentId   bigint                             null comment '父标签 id',
    isParent   tinyint                            null comment '0 -不是，1 -父标签',
    createTime datetime default CURRENT_TIMESTAMP null comment '创建时间',
    updateTime datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '更新时间',
    isDelete   tinyint  default 0                 not null comment '是否删除'
)
    comment '标签';
```



### 3. 队伍表 `team`

​	用于存储队伍信息

**字段**

1. id 主键
2. name 队伍名称
3. description 队伍描述
4. expireTime 超时时间
5. userId 创建者（队长）id 逻辑外键
6. status 状态 0-公开，1-私有，2-加密
7. password 私有队伍密码
8. createTime 创建时间
9. updateTIme 更新时间
10. isDelete 逻辑删除 1-已删除



**建表语句**

```sql
create table user_team
(
    id         bigint auto_increment comment

[...截断...]

 'id'
        primary key,
    userId     bigint                             null comment '用户id',
    teamId     bigint                             null comment '队伍id',
    joinTime   datetime                           null comment '加入时间',
    createTime datetime default CURRENT_TIMESTAMP null comment '创建时间',
    updateTime datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    isDelete   tinyint  default 0                 not null comment '是否删除'
)
    comment '用户队伍关系';
```



### 4. 用户队伍关系表 `user_team`

​	用于存放队伍对应的成员信息

**字段**

1. id 主键
2. userId 用户id 逻辑外键
3. teamId 队伍id 逻辑外键
4. joinTIme 加入时间
5. createTime 创建时间
6. updateTime 更新时间
7. isDelete 逻辑删除 1-已删除



**建表语句**

```sql
create table user_team
(
    id         bigint auto_increment comment 'id'
        primary key,
    userId     bigint                             null comment '用户id',
    teamId     bigint                             null comment '队伍id',
    joinTime   datetime                           null comment '加入时间',
    createTime datetime default CURRENT_TIMESTAMP null comment '创建时间',
    updateTime datetime default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    isDelete   tinyint  default 0                 not null comment '是否删除'
)
    comment '用户队伍关系';
```



### 5. 粉丝关注表 `follow_relationship`

​	存储用户关注的用户以及粉丝

**字段**

1. id 主键
2. follower_id 关注者id 逻辑外键
3. followed_id 被关注者id 逻辑外键
4. create_time 创建时间
5. is_delete 逻辑删除 1-已删除



**建表语句**

```sql
create table follow_relationship
(
    id          bigint auto_increment
        primary key,
    follower_id bigint                             not null comment '关注者ID',
    followed_id bigint                             not null comment '被关注者ID',
    create_time datetime default CURRENT_TIMESTAMP null comment '关注时间',
    is_delete   tinyint  default 0                 null comment '是否删除'
)
    comment '粉丝关注关系';
```



### 6. 私聊信息表 `chat_messages`

​	存储用户私聊消息数据

**字段**

1. chat_id 主键
2. sender_id 发送者id 逻辑外键
3. receiver_id 接收者id 逻辑外键
4. timestamp 发送时间
5. read_status 已读状态 0-未读，1-已读



**建表语句**

```sql
create table chat_messages
(
    chat_id     int auto_increment comment '唯一标识'
        primary key,
    sender_id   int                                  null comment '发送者id',
    receiver_id int                                  null comment '接收者id',
    message     text                                 null comment '消息内容',
    timestamp   timestamp  default CURRENT_TIMESTAMP not null comment '发送时间',
    read_status tinyint(1) default 0                 null comment '状态：0-未读，1-已读'
)
    comment '用户私聊消息表';
```



### 7. 用户在线状态表 `user_online_status`

​	存储用户在线信息

**字段**

1. user_id 用户id 主键 逻辑外键
2. is_online 状态 0-离线，1-在线
3. last_online 最后在线时间



**建表语句**

```sql
create table user_online_status
(
    user_id     bigint                               not null comment '用户id'
        primary key,
    is_online   tinyint(1) default 0                 null comment '状态，0-离线，1-在线',
    last_online timestamp  default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '最后在线时间'
)
    comment '用户在线状态表';
```



## 配置

### 登录态存储

​	登录态 Session 共享，当项目多机部署时，将用户登录态保存在 Redis 数据库中，实现共享登录态

选择 Redis 存储 Session 的原因：基于内存的 K / V 数据库，用户信息读取 / 是否登录的判断极其**频繁** ，Redis 基于内存，读写性能很高。

1. 引入 redis，能够操作 redis：

   ```xml
   <!-- https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-data-redis -->
   <dependency>
       <groupId>org.springframework.boot</groupId>
       <artifactId>spring-boot-starter-data-redis</artifactId>
       <version>2.6.4</version>
   </dependency>
   ```

2. 引入 spring-session 和 redis 的整合，使得自动将 session 存储到 redis 中：

   ```xml
   <!-- https://mvnrepository.com/artifact/org.springframework.session/spring-session-data-redis -->
   <dependency>
       <groupId>org.springframework.session</groupId>
       <artifactId>spring-session-data-redis</artifactId>
       <version>2.6.3</version>
   </dependency>
   ```

3. 修改 spring-session 存储配置 `spring.session.store-type`

   - 默认是 none，表示存储在单台服务