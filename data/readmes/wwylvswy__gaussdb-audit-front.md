## 简介
GaussDB智能评审助手的前端代码，不包含知识库管理模块。

## 目录
- [项目的基本目录结构](https://pure-admin.cn/pages/directory/)
- 新增文件介绍
```bash
├── src
│   ├── api  # 接口请求统一管理
|   |   |—— user.ts   #用户管理请求接口
|   |   |—— audit.ts  #评审请求接口
|   |   |—— ogdl.ts   #数据源管理和直连数据库请求接口
|   |   |—— routes.ts   #菜单请求接口
│   ├── components  # 自定义通用组件
│   │   ├── ReAnalisys  #评审直方图和饼状图组件
│   ├── views  # 存放编写业务代码页面
|   |   |—— audit/   #评审页面
|   |   |—— dashbord/   #系统首页
|   |   |—— syssettings/    #系统设置
```

## 运行
```bash
# 全局安装pnpm
npm install -g pnpm

# 安装依赖
pnpm install

# 启动
pnpm dev
```

## Pure Admin配套视频
[点我查看 UI 设计](https://www.bilibili.com/video/BV17g411T7rq)  
[点我查看快速开发教程](https://www.bilibili.com/video/BV1kg411v7QT)

## Pure Admin 配套使用文档
[点我查看 vue-pure-admin 文档](https://pure-admin.cn/)  
[点我查看 @pureadmin/utils 文档](https://pure-admin-utils.netlify.app)
