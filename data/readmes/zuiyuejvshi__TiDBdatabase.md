# 外贸发货看板 / International Shipment Dashboard

这是一个基于 Jekyll 的静态网站，用于管理和追踪国际货物运输。该系统允许贸易商创建和跟踪运单，客户可以查看其订单的状态更新。

## 功能特点

- **运单追踪**：查看所有运单及其当前状态
- **状态筛选**：按状态（未发货、已发货、已到达、已提货）筛选运单
- **客户信息**：查看客户详细信息，包括联系方式和时区
- **详细视图**：每个运单的详细信息页面和时间线
- **添加新运单**：添加新运单的表单
- **团队介绍**：展示开发团队成员信息

## 项目结构

- `_data/`：包含 YAML 格式的数据文件
  - `clients.yml`：客户信息
  - `shipments.yml`：运单信息
  - `navigation.yml`：导航菜单结构
  - `team.yml`：团队成员信息
- `_sass/`：包含 SCSS 样式文件
  - `main.scss`：主样式文件
  - `navigation.scss`：导航样式
  - `home.scss`：首页样式
  - `about.scss`：关于页面样式
  - `shipments.scss`：运单列表页面样式
  - `shipment-detail.scss`：运单详情页面样式
  - `add-shipment.scss`：添加运单页面样式
  - `team.scss`：团队页面样式
- 页面：
  - `index.html`：主页，显示运单概览
  - `about.md`：关于页面，介绍系统
  - `shipments.html`：运单列表页面
  - `shipment_detail.html`：单个运单的详细视图
  - `add_shipment.html`：添加新运单的表单
  - `staff.html`：团队成员介绍

## 本地开发

1. 确保安装了 Ruby 和 Jekyll
2. 克隆此仓库
3. 运行 `bundle install` 安装依赖
4. 运行 `bundle exec jekyll serve` 启动开发服务器
5. 在浏览器中访问 `http://localhost:4000` 查看网站

## 使用的技术

- Jekyll（静态站点生成器）
- Liquid（模板语言）
- SCSS（样式）
- JavaScript（客户端交互）

## 后续改进计划

- 用户认证系统，区分贸易商和客户
- 添加更新运单状态的功能
- 实现状态变更的邮件通知
- 多语言支持，适应国际客户
- 时区转换，以准确显示发货时间
- 为运单附加文档的上传功能