# vue-mute-table 多维表格编辑器

![](./vue-table.gif)

## 项目介绍

多维表格编辑器是一个基于 Vue 3 的高性能数据表格应用，支持虚拟滚动、海量数据处理、多视图展示和实时编辑。该项目采用现代化的前端技术栈，提供了类似 Airtable 或 Notion 的表格编辑体验。

## 在线办公相关解决方案

1. [flowmix/docx多模态文档编辑器](https://flowmix.turntip.cn)
2. [灵语AI文档](https://mindlink.turntip.cn)
3. [flowmixAI智能办公工作台](https://ai.flowmix.cn)
4. [pxcharts多维表格](http://pxcharts.com)

## 技术栈

### 核心框架
- **Vue 3.4.15** - 渐进式 JavaScript 框架，采用 Composition API
- **TypeScript 5.3.3** - 提供类型安全和更好的开发体验
- **Vite 5.0.12** - 快速的前端构建工具，支持热重载

### 状态管理
- **Pinia 2.1.7** - Vue 3 官方推荐的状态管理库
- **pinia-plugin-persistedstate 3.2.1** - 状态持久化插件

### 路由管理
- **Vue Router 4.2.5** - Vue 官方路由管理器

### UI 组件与样式
- **Tailwind CSS 3.4.1** - 实用优先的 CSS 框架
- **Lucide Vue Next 0.312.0** - 现代化图标库
- **@tailwindcss/forms** - 表单样式增强
- **@tailwindcss/typography** - 排版样式
- **@tailwindcss/aspect-ratio** - 宽高比工具

### 数据处理与工具
- **Lodash-es 4.17.21** - JavaScript 实用工具库
- **Date-fns 3.3.1** - 现代 JavaScript 日期工具库
- **Nanoid 5.0.4** - 小巧的唯一 ID 生成器
- **Mitt 3.0.1** - 轻量级事件发射器

### 文件处理
- **PapaParse 5.4.1** - CSV 解析库
- **XLSX 0.18.5** - Excel 文件处理
- **JSZip 3.10.1** - ZIP 文件处理
- **File-saver 2.0.5** - 文件下载工具

### 虚拟化与性能
- **Vue Virtual Scroller 2.0.0-beta.8** - Vue 虚拟滚动组件
- **Virtual-list 1.0.1** - 虚拟列表实现
- **Intersection Observer 0.12.2** - 交叉观察器 API
- **Resize Observer Polyfill 1.5.1** - 尺寸变化观察器

### 拖拽与排序
- **SortableJS 1.15.1** - 拖拽排序库

### 搜索功能
- **Fuse.js 7.0.0** - 模糊搜索库

### 图表与可视化
- **Chart.js 4.4.1** - 图表库
- **Vue ChartJS 5.3.0** - Vue Chart.js 集成

### 开发工具
- **ESLint** - 代码质量检查
- **Prettier** - 代码格式化
- **Stylelint** - CSS 代码检查
- **Husky** - Git hooks 管理
- **Lint-staged** - 暂存文件检查
- **Commitizen** - 规范化提交信息

### 测试框架
- **Vitest 1.2.2** - 快速单元测试框架
- **@vue/test-utils** - Vue 组件测试工具

### PWA 支持
- **Vite Plugin PWA 0.17.4** - 渐进式 Web 应用支持

### 自动导入
- **unplugin-auto-import** - 自动导入 API
- **unplugin-vue-components** - 自动导入组件

## 架构设计

### 整体架构

项目采用分层架构设计，主要分为以下几个层次：

```
┌─────────────────────────────────────────┐
│                视图层 (Views)            │
│  TableView | KanbanView | FormView      │
├─────────────────────────────────────────┤
│               组件层 (Components)        │
│  VirtualTable | TableToolbar | Modals   │
├─────────────────────────────────────────┤
│               状态层 (Stores)            │
│           Pinia Store (table.ts)        │
├─────────────────────────────────────────┤
│               工具层 (Utils)             │
│        工具函数 | 类型定义 | 常量          │
├─────────────────────────────────────────┤
│               数据层 (Data)              │
│     本地存储 | 导入导出 | 数据处理          │
└─────────────────────────────────────────┘
```

### 核心模块

#### 1. 状态管理 (Pinia Store)
- **数据模型**: 字段(Field)、记录(Record)、视图(View)
- **状态管理**: 表格数据、筛选、排序、分组
- **持久化**: 自动保存到 localStorage
- **响应式**: 基于 Vue 3 的响应式系统

#### 2. 虚拟滚动系统
- **性能优化**: 只渲染可见区域的 DOM 元素
- **动态计算**: 根据滚动位置动态计算可见行
- **分组支持**: 支持分组数据的虚拟滚动
- **内存管理**: 自动回收不可见的 DOM 元素

#### 3. 组件架构
- **原子化设计**: 每个组件职责单一
- **组合式 API**: 使用 Vue 3 Composition API
- **类型安全**: 完整的 TypeScript 类型定义
- **可复用性**: 高度可配置和可扩展

### 数据流

```
用户操作 → 组件事件 → Store Actions → 状态更新 → 视图响应
    ↓
本地存储 ← 数据持久化 ← 状态变化监听
```

## 项目功能亮点

### 1. 高性能虚拟滚动
- **海量数据处理**: 支持数万条记录的流畅滚动
- **内存优化**: 只渲染可见区域，大幅降低内存占用
- **分组虚拟化**: 支持分组数据的虚拟滚动
- **自适应高度**: 根据容器大小自动调整

### 2. 多视图支持
- **表格视图**: 传统的数据表格展示
- **看板视图**: 卡片式任务管理界面
- **表单视图**: 单条记录的详细编辑
- **视图切换**: 无缝切换不同视图模式

### 3. 灵活的字段系统
- **多种字段类型**: 文本、数字、日期、选择、用户等
- **动态字段管理**: 运行时添加、删除、修改字段
- **字段验证**: 内置数据验证规则
- **字段配置**: 宽度、可见性、必填等配置

### 4. 强大的数据处理
- **实时筛选**: 多条件组合筛选
- **多级排序**: 支持多字段排序
- **数据分组**: 按字段值自动分组
- **搜索功能**: 模糊搜索支持

### 5. 拖拽交互
- **列拖拽**: 调整列顺序
- **行拖拽**: 调整行顺序
- **列宽调整**: 鼠标拖拽调整列宽
- **分组内排序**: 支持分组内的拖拽排序

### 6. 数据导入导出
- **多格式支持**: CSV、Excel、JSON 格式
- **批量导入**: 支持大量数据导入
- **数据导出**: 一键导出所有数据
- **格式转换**: 自动处理不同数据格式

### 7. 响应式设计
- **移动端适配**: 完整的移动端支持
- **自适应布局**: 根据屏幕尺寸调整布局
- **触摸优化**: 移动端触摸交互优化

### 8. 性能监控
- **实时监控**: 渲染性能实时监控
- **内存使用**: 内存占用情况监控
- **性能指标**: FPS、渲染时间等指标

## 二次开发指南

### 环境要求
- Node.js >= 18.0.0
- npm >= 8.0.0 或 pnpm
- 现代浏览器支持

### 开发环境搭建

1. **克隆项目**
```bash
git clone https://github.com/MrXujiang/vue-mute-table
cd vue-mute-table
```

2. **安装依赖**
```bash
# 使用 pnpm (推荐)
pnpm install

# 或使用 npm
npm install
```

3. **启动开发服务器**
```bash
pnpm dev
# 或
npm run dev
```

4. **构建生产版本**
```bash
pnpm build
# 或
npm run build
```

### 项目结构

```
src/
├── components/           # 组件目录
│   ├── modals/          # 模态框组件
│   ├── VirtualTable.vue # 虚拟表格组件
│   ├── TableToolbar.vue # 表格工具栏
│   └── ...
├── views/               # 页面组件
│   ├── TableView.vue    # 表格视图
│   ├── KanbanView.vue   # 看板视图
│   └── FormView.vue     # 表单视图
├── stores/              # 状态管理
│   └── table.ts         # 表格状态
├── types/               # 类型定义
│   └── index.ts         # 核心类型
├── utils/               # 工具函数
│   └── index.ts         # 通用工具
├── router/              # 路由配置
│   └── index.ts         # 路由定义
├── styles/              # 样式文件
│   └── variables.scss   # SCSS 变量
└── main.ts              # 应用入口
```

### 核心组件说明

#### VirtualTable 组件
虚拟表格的核心组件，负责：
- 虚拟滚动实现
- 列管理
- 行渲染
- 交互处理

```typescript
// 使用示例
<VirtualTable
  :container-height="600"
  :row-height="48"
  :overscan="5"
  :group-header-height="40"
/>
```

#### TableStore 状态管理
Pinia store，管理所有表格相关状态：

```typescript
// 主要状态
const {
  fields,           // 字段列表
  records,          // 记录列表
  views,            // 视图列表
  currentViewId,    // 当前视图ID
  selectedRecords,  // 选中的记录
  editingCell,      // 正在编辑的单元格
  filters,          // 筛选条件
  sorts,            // 排序条件
  groupBy,          // 分组字段
} = useTableStore()
```

### 开发规范

#### 1. 代码风格
- 使用 ESLint + Prettier 统一代码风格
- 遵循 Vue 3 Composition API 最佳实践
- 使用 TypeScript 严格模式

#### 2. 组件开发
- 使用 `<script setup>` 语法
- 定义完整的 TypeScript 类型
- 组件名使用 PascalCase
- 文件名使用 PascalCase.vue

#### 3. 状态管理
- 使用 Pinia 进行状态管理
- 状态更新使用 actions
- 计算属性使用 computed
- 副作用使用 watch

#### 4. 样式规范
- 使用 Tailwind CSS 工具类
- 自定义样式使用 SCSS
- 响应式设计优先
- 移动端适配

### 扩展开发

#### 1. 添加新字段类型
```typescript
// 在 types/index.ts 中扩展字段类型
export interface Field {
  type: "text" | "number" | "date" | "select" | "multiSelect" | "user" | "checkbox" | "url" | "email" | "phone" | "yourNewType"
  // ... 其他属性
}

// 在 utils/index.ts 中添加图标映射
export function getFieldIcon(type: string): string {
  const iconMap: Record<string, string> = {
    // ... 现有映射
    yourNewType: "YourIcon"
  }
  return iconMap[type] || "Type"
}
```

#### 2. 添加新视图类型
```typescript
// 在 types/index.ts 中扩展视图类型
export interface View {
  type: "table" | "kanban" | "calendar" | "form" | "yourNewView"
  // ... 其他属性
}

// 创建新的视图组件
// src/views/YourNewView.vue
```

#### 3. 自定义筛选器
```typescript
// 在 stores/table.ts 中扩展筛选逻辑
const filteredRecords = computed(() => {
  // ... 现有筛选逻辑
  // 添加你的自定义筛选逻辑
})
```

#### 4. 添加新的导入导出格式
```typescript
// 在 utils/index.ts 中添加新的处理函数
export function importYourFormat(data: string): Record[] {
  // 实现你的导入逻辑
}

export function exportYourFormat(records: Record[]): string {
  // 实现你的导出逻辑
}
```

### 性能优化建议

#### 1. 虚拟滚动优化
- 合理设置 `overscan` 参数
- 避免在渲染过程中进行复杂计算
- 使用 `will-change` CSS 属性

#### 2. 状态管理优化
- 使用 `shallowRef` 处理大型对象
- 避免不必要的响应式转换
- 合理使用 `computed` 缓存计算结果

#### 3. 组件优化
- 使用 `v-memo` 缓存复杂组件
- 合理使用 `v-show` 和 `v-if`
- 避免在模板中使用复杂表达式

### 调试工具

#### 1. Vue DevTools
- 安装 Vue DevTools 浏览器扩展
- 查看组件状态和 props
- 监控状态变化

#### 2. 性能监控
- 使用浏览器 Performance 面板
- 监控内存使用情况
- 分析渲染性能

#### 3. 开发工具
```bash
# 类型检查
pnpm type-check

# 代码检查
pnpm lint

# 样式检查
pnpm lint:style

# 测试
pnpm test
```

### 部署指南

#### 1. 构建配置
```typescript
// vite.config.ts 中的构建配置
build: {
  target: "es2015",
  outDir: "dist",
  assetsDir: "assets",
  sourcemap: false,
  minify: "terser",
  rollupOptions: {
    output: {
      manualChunks: {
        // 手动分包配置
      }
    }
  }
}
```

#### 2. 环境变量
```bash
# .env.production
VITE_API_BASE_URL=https://your-api-domain.com
```

#### 3. 部署步骤
```bash
# 构建生产版本
pnpm build

# 部署到服务器
# 将 dist 目录内容上传到 Web 服务器
```

### 常见问题

#### 1. 虚拟滚动性能问题
- 检查 `rowHeight` 设置是否正确
- 确保容器高度设置合理
- 避免在滚动过程中进行重计算

#### 2. 状态同步问题
- 确保使用 `reactive` 或 `ref` 包装响应式数据
- 检查状态更新的时机
- 使用 `nextTick` 确保 DOM 更新完成

#### 3. 类型错误
- 确保所有接口都有正确的类型定义
- 使用 `as` 断言处理类型转换
- 检查导入的类型是否正确

### 联系方式

- 作者: 徐小夕
- 微信: cxzk_168
- 技术分享公众号: 趣谈AI

---

*本文档持续更新，如有问题请提交 Issue 或联系维护者。*