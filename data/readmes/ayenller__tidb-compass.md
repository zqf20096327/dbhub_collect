# TiDB Compass

TiDB Compass 是一个面向销售、售前和伙伴介绍场景的 iOS 风格多语言 APP 壳示例。

当前支持语言：

- 中文
- 日文
- 英文
- 葡萄牙语
- 西班牙语

## 文件结构

- `index.html`：TiDB Compass iOS APP 壳
- `assets/app.css`：APP 壳样式
- `assets/app.js`：APP 壳交互与语言切换
- `content/tidb-sales-kit.html`：内嵌静态介绍页，按语言参数动态渲染
- `ios/TiDBCompass.xcodeproj`：原生 iOS 工程
- `ios/TiDBCompass/`：SwiftUI + WKWebView 应用代码
- `ios/content/tidb-sales-kit.html`：随 iOS App 打包的页面资源
- `ios/TiDBCompass/Branding/tidb-logo.svg`：从 PingCAP 官方站点拉取的 TiDB logo 源文件，用于生成 App Icon

## 使用方式

直接在浏览器打开 `index.html` 即可预览。

当前预览支持：

- iPhone / iPad 切换
- 横版 / 竖版切换
- 中文、日文、英文、葡萄牙语、西班牙语切换
- 底部 Tab Bar 的 iOS 应用式页面预览

当前版本已收敛到设计定稿预览，可作为后续转 SwiftUI、React Native 或 WebView 壳实现的视觉基线。

## iOS 项目

已迁移出一个可构建的原生 iOS 工程：

- SwiftUI 负责原生头部与语言切换
- SwiftUI 原生设置页负责语言与预览上下文查看
- SwiftUI 原生 Tab 已拆出 Preview / About 两个入口
- WKWebView 负责加载设计定稿页面
- 页面上下文会由原生层注入：语言、iPhone/iPad、横版/竖版
- 已补基础 Launch Screen 与 App Icon 资源位，便于继续朝可发布工程推进

### 打开方式

直接用 Xcode 打开：

- `ios/TiDBCompass.xcodeproj`

### 命令行构建

```bash
xcodebuild -project ios/TiDBCompass.xcodeproj \
  -scheme TiDBCompass \
  -configuration Debug \
  -sdk iphonesimulator \
  -destination 'generic/platform=iOS Simulator' \
  CODE_SIGNING_ALLOWED=NO build
```

### 资源同步

iOS 工程当前打包使用的是：

- `ios/content/tidb-sales-kit.html`

如果你继续修改网页设计稿，请同步更新一份到 iOS 资源目录：

```bash
cp content/tidb-sales-kit.html ios/content/tidb-sales-kit.html
```

## 更新内容

后续如果需要由后台持续更新介绍内容，优先更新 `content/tidb-sales-kit.html` 的语言内容数据。
这样可以保持 APP 壳稳定，同时持续迭代页面文案与模块。
