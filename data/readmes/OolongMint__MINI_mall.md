# Mini Mall

一个可以本地运行的中文微型电商，包含响应式商城、用户账号、购物车、地址簿、模拟支付、订单履约和管理后台。商品使用项目内置 SVG 插画，无需图片服务。

## 技术栈

- Next.js 16 App Router / React 19 / TypeScript
- Prisma **5.22.0** 与 SQLite（Node.js runtime）
- TailwindCSS 4 / Lucide 图标 / Zod 4
- bcrypt 密码哈希、数据库会话与 HttpOnly Cookie
- Node.js test runner 业务集成测试、Playwright 桌面及移动端测试

已在 Windows PowerShell、Node.js **24.15.0** 和 npm **11.12.1** 上完成安装、迁移、业务测试与生产构建。推荐使用 Node.js 24 LTS；Next.js 16 最低要求 Node.js 20.9。

环境示例默认关闭 Next.js 遥测，避免构建依赖用户目录中的全局遥测配置文件。

## 本地启动

在本 README 所在目录运行（本项目位于工作区根目录）：

```powershell
npm ci
Copy-Item .env.example .env
npm run db:setup
npm run dev
```

打开 [http://localhost:3000](http://localhost:3000)。macOS / Linux 可用 `cp .env.example .env` 复制环境文件。

`db:setup` 会生成 Prisma Client、应用迁移并初始化演示数据。再次执行不会重置已有账号密码、库存、商品编辑或订单。开发数据库在 `prisma/dev.db`，默认配置为 `DATABASE_URL="file:./dev.db"`，路径相对于 Prisma schema。SQLite 文件和 `.env` 已忽略，不应提交。

### 演示账号

| 角色 | 邮箱 | 密码 |
| --- | --- | --- |
| 管理员 | admin@minimall.local | MiniMall123! |
| 普通用户 | hello@minimall.local | MiniMall123! |

种子数据包含 4 个分类、14 件商品（含售罄商品）及普通用户的演示地址。普通用户还可以自行注册；注册不能指定管理员角色。管理员登录后进入 `/admin`，也可从账户菜单进入。

以上凭据仅供本地演示。首版不包含邮件验证、密码找回和真实支付。

## 使用流程

1. 在首页或 `/products` 浏览商品；列表支持名称搜索、分类筛选及分页，条件保存在 URL。
2. 注册或登录后在详情页加购，在 `/cart` 修改数量或移除商品。
3. 在 `/account/addresses` 新增收货地址；返回 `/checkout` 选择地址并提交整个购物车。
4. 在订单详情确认模拟支付，或取消待支付订单。模拟支付不会真实扣款。
5. 使用另一个浏览器或无痕窗口登录管理员，在 `/admin/orders` 找到已支付订单并确认发货。
6. 用户刷新订单详情，确认收货完成交易。

后台商品支持新增、编辑、上下架及删除；分类支持新增、改名和删除。图片可填写 `http(s)` URL 或 `/images/mug.svg` 等内置素材路径，不支持上传。外部图片的可用性由其提供方决定。

## 业务规则

- 单商家、单规格、人民币整数分计价，全场免运费。访客可浏览，登录后才能使用购物车与结算。
- 添加购物车不预留库存。下单在事务内重新读取商品价格、校验库存与上架状态、扣减库存、保存订单快照并清空购物车，任一商品不满足条件则整单回滚。
- 购物车单件商品最多 999 件，最多保存 20 个收货地址。已保存地址始终保留一个默认地址。
- 订单保存商品名称、图片、单价及收货地址快照，后续商品编辑、调价或地址删除不会影响历史订单。
- 状态流转：`PENDING_PAYMENT → PAID → SHIPPED → COMPLETED`；`PENDING_PAYMENT → CANCELLED`。只允许用户操作自己的订单，发货只允许管理员操作。
- 同一请求标识只创建一笔订单，重复支付、发货、确认收货和取消具有幂等性。取消在事务内恢复库存，不会重复恢复。无自动超时取消，待支付订单需手动支付或取消。
- 有订单关联的商品删除时归档并下架，保留历史关系；其他商品物理删除并清理购物车。归档商品可在后台“已归档”筛选中编辑分类，但不能重新上架。
- 有商品关联（包含归档商品）的分类不可删除；请先编辑这些商品并迁移到其他分类。
- 用户及后台页面按请求动态读取。服务端检查身份、角色及资源归属；客户端提交的总价、角色和订单状态均不能直接生效。会话有效期 7 天，数据库仅保存随机会话令牌的 SHA-256 摘要；退出即撤销会话。

## 项目结构

```text
src/app/                商城、账号、订单与后台页面
src/components/         表单反馈、商品卡片、订单展示等组件
src/lib/services.ts     事务、库存、订单、账号与管理业务
src/lib/actions.ts      Server Actions、权限入口与数据刷新
src/lib/auth.ts         请求级会话、登录与管理员检查
src/lib/validation.ts   Zod 服务端输入校验
prisma/                 模型、可重复执行种子与初始迁移
public/images/          本地商品与首页 SVG 素材
tests/                  业务集成测试和浏览器测试
```

不提供公共 REST API；服务端组件读取数据，Server Actions 提交变更。本地 SQLite 使用单实例文件，不适用于无持久化文件系统的托管环境。

## 检查与测试

```powershell
npm run lint
npm run typecheck
npm test
npm run build
```

业务测试自动在独立的 `prisma/test.db` 上应用迁移并清理测试数据，覆盖注册登录、会话过期、权限、地址归属、库存不足、金额计算、快照、事务回滚、最后库存争抢、并发重复下单、取消幂等与后台 CRUD。不会清理开发数据库。

浏览器测试首次需准备 Chromium：

```powershell
npx playwright install chromium
npm run test:e2e
```

Playwright 每次运行先重建并初始化独立的 `prisma/e2e.db`，再在 `127.0.0.1:3100` 启动专用开发服务，运行桌面与手机 Chromium 场景；包括注册购买全流程、管理员发货、商品分类 CRUD、筛选分页、空状态和手机首页无横向溢出。重建脚本校验数据库路径，拒绝操作开发数据库。端口必须空闲；本次测试数据保留到下次运行，便于排查。首页截图、失败截图和 trace 位于 `test-results/`，可用 `npx playwright show-trace <trace.zip>` 查看。

Next.js 16 的 `next build` 不会自动执行 ESLint，因此 lint 是独立命令。若工作区含其他独立项目，它们不属于本项目的 TypeScript / ESLint 检查范围。

## 数据库维护与生产构建

```powershell
# 修改 schema 后创建开发迁移，并提交生成的 SQL
npx prisma migrate dev --name describe_change

# 应用已提交迁移
npm run db:migrate

# 查看数据
npx prisma studio

# 清空当前数据库并重新迁移、初始化：会删除全部当前数据
npm run db:reset

# 本地验证生产模式
npm run build
npm start
```

重置前请停止应用并备份 `prisma/dev.db`。重置使用当前 `DATABASE_URL`，请先检查 `.env`。测试期间避免让不同服务共用同一个数据库或 `.next` 目录。

`npm start` 使用生产模式，会话 Cookie 带 `Secure`。浏览器通常对 `localhost` 有本地安全例外；如本机浏览器不接受该 Cookie，请使用 `npm run dev` 测试登录，或在 HTTPS 下运行生产服务。首版交付目标为本地演示，不包含线上部署、真实物流、退款售后、优惠券与多规格。
