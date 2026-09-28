# 期货数据库系统

完整的国内期货数据库，存储所有期货品种的主力连续合约数据和历史价格、新闻资讯。

## 🚀 快速安装

### 方式一：一键安装（推荐）

```bash
npx skills add canqihe/futures-data-skill
```

安装后，在 Claude Code 中直接使用：

```
"为什么螺纹钢最近跌了？"
"查询RB0最近一周的表现"
"哪些黑色系品种成交量最大？"
```

### 方式二：手动安装

```bash
# 克隆仓库
git clone https://github.com/canqihe/futures-data-skill.git ~/.claude/skills/futures-trader

# 安装依赖
cd ~/.claude/skills/futures-trader
pip install -r requirements.txt
```

## 📊 数据概览

- **66个期货品种** - 覆盖6大交易所
- **187,550条OHLCV记录** - 数据范围：2005-01-04 至 2026-03-20
- **15,166条新闻资讯** - 实时市场动态
- **支持查询、分析、统计** - 智能涨跌分析，新闻关联

## ⚠️ 重要提示

**数据库文件未包含在仓库中** - 由于数据库文件较大（46MB），且会持续更新，因此未提交到git仓库。

**首次使用需要初始化数据库**：
```bash
cd ~/.claude/skills/futures-trader

# 方式1：完整初始化（推荐，需要10-20分钟）
python3 scripts/init_db.py
python3 scripts/fetch_initial_data.py

# 方式2：快速测试（只获取几个品种，1-2分钟）
python3 scripts/init_db.py
python3 -c "
from backend.updater import FuturesUpdater
updater = FuturesUpdater()
updater.update_all_ohlc(symbols=['RB0', 'CU0', 'JM0', 'AU0'])
updater.close()
"
```

## 项目结构

```
~/.claude/skills/futures-trader/
├── skill.md                # Skill主文件（完整使用说明）
├── futures.db              # SQLite数据库
├── backend/
│   ├── __init__.py
│   ├── database.py         # 数据库连接和初始化
│   ├── collector.py        # 数据采集
│   ├── updater.py          # 批量更新
│   └── constants.py        # 常量定义（品种列表、映射）
├── scripts/
│   ├── init_db.py          # 初始化数据库
│   ├── fetch_initial_data.py  # 获取初始数据
│   └── daily_update.py     # 每日更新脚本
├── requirements.txt        # 依赖包
└── README.md              # 本文档
```

## 数据库设计

### 表结构

1. **futures_tickers** - 期货品种主表
   - symbol: 主力连续合约代码
   - name: 品种名称
   - exchange: 交易所
   - sector: 所属板块
   - last_ohlc_fetch: 最后获取价格数据的时间
   - last_news_fetch: 最后获取新闻的时间

2. **futures_ohlc** - 历史价格表
   - symbol, date, open, high, low, close
   - volume: 成交量
   - hold: 持仓量
   - settle: 结算价
   - amount: 成交额（自动计算：成交量 × 结算价 × 合约乘数）

3. **futures_contracts** - 合约乘数表
   - symbol: 合约代码
   - name: 品种名称
   - multiplier: 合约乘数（每手合约的单位数量）
   - unit: 计价单位
   - exchange: 交易所

4. **futures_news_raw** - 原始新闻表
   - id: 唯一ID（MD5哈希）
   - title: 标题
   - content: 内容
   - publisher: 来源
   - published_utc: 发布时间（UTC）

5. **futures_news_ticker** - 新闻-品种关系表

### 当前数据统计

- **品种数量**: 66个
- **交易所分布**:
  - 大连商品交易所 (DCE): 20个
  - 郑州商品交易所 (CZCE): 17个
  - 上海期货交易所 (SHFE): 14个
  - 中国金融期货交易所 (CFFEX): 8个
  - 上海国际能源交易中心 (INE): 5个
  - 广州期货交易所 (GFEX): 2个

- **数据范围**: 2005-01-04 至 2026-03-20
- **OHLCV记录**: 187,550条
- **新闻资讯**: 15,166条

## 使用方法

### 1. 安装依赖

```bash
cd ~/.claude/skills/futures-trader
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python3 scripts/init_db.py
```

### 3. 获取初始数据（可选）

```bash
python3 scripts/fetch_initial_data.py
```

### 4. 每日更新

```bash
python3 scripts/daily_update.py
```

### 5. 设置定时任务

编辑 crontab：
```bash
crontab -e
```

添加每日18点自动更新（工作日）：
```
0 18 * * 1-5 cd ~/.claude/skills/futures-trader && python3 scripts/daily_update.py
```

## API 接口

### Python API

```python
import sys
sys.path.insert(0, '~/.claude/skills/futures-trader')

from backend.updater import FuturesUpdater
from backend.database import get_conn

# 创建更新器
updater = FuturesUpdater()

# 更新所有品种的OHLCV数据
results = updater.update_all_ohlc()

# 更新新闻数据
news_results = updater.update_all_news()

# 获取数据库统计
stats = updater.get_db_stats()

# 查询数据
conn = get_conn()
df = pd.read_sql_query('SELECT * FROM futures_ohlc WHERE symbol="RB0"', conn)
```

### SQL 查询示例

```sql
-- 查询品种数量
SELECT COUNT(*) FROM futures_tickers;

-- 查询每个品种的数据统计
SELECT symbol, COUNT(*) as count, MIN(date), MAX(date)
FROM futures_ohlc
GROUP BY symbol;

-- 查询最新价格（包含涨跌幅）
WITH daily_change AS (
    SELECT
        symbol,
        date,
        close,
        LAG(close) OVER (PARTITION BY symbol ORDER BY date) as prev_close
    FROM futures_ohlc
)
SELECT
    symbol,
    date,
    close,
    ROUND((close - prev_close) / prev_close * 100, 2) as change_pct
FROM daily_change
WHERE prev_close IS NOT NULL
ORDER BY date DESC
LIMIT 10;

-- 查询新闻
SELECT * FROM futures_news_raw
ORDER BY published_utc DESC
LIMIT 10;
```

## Skill 使用

### 在 Claude Code 中使用

```bash
# 查询期货价格
"查询RB0最近一周的表现"

# 分析涨跌原因
"为什么焦煤最近跌了？"

# 板块统计
"哪些黑色系品种成交量最大？"

# 品种推荐
"推荐几个活跃的有色金属品种"

# 更新数据
"更新期货数据"
```

详细使用说明请查看 `skill.md` 文件。

## 数据源

- **价格数据**: AKShare (新浪财经)
  - `ak.futures_zh_daily_sina()`
- **新闻数据**: AKShare (上海金属网)
  - `ak.futures_news_shmet()`

## 注意事项

1. **API限流**: 每次请求间隔1-2秒，避免被限流
2. **数据更新**: 建议工作日18点后更新（收盘后）
3. **错误处理**: 脚本会自动重试失败的请求（最多3次）
4. **增量更新**: 只插入新数据，不会重复插入

## 故障排除

### 问题：无法获取数据

- 检查网络连接
- 确认AKShare版本：`pip show akshare`
- 部分期货品种可能已退市或暂无数据

### 问题：数据库文件损坏

```bash
rm ~/.claude/skills/futures-trader/futures.db
python3 scripts/init_db.py
```

## 项目参考

- PokieTicker 股票数据库: `/Users/colin/Desktop/File/PokieTicker-main/`
- AKShare 文档: https://akshare.akfamily.xyz/

## 声明

本系统提供的数据和分析仅供参考，不构成任何投资建议。期货交易有风险，投资需谨慎。
