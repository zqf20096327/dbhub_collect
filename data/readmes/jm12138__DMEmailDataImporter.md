# DMEmailDataImporter

一个用于自动接收邮件附件表格数据并导入达梦数据库的定时任务工具。

## 功能特性

- 🔄 **定时任务执行**：支持 Cron 表达式配置定时任务
- 📧 **邮件附件获取**：自动连接邮箱获取指定主题的邮件附件
- 📊 **Excel 数据解析**：支持解析 Excel 文件中的表格数据
- 🗄️ **数据库批量导入**：自动将数据批量插入到达梦数据库
- ⚡ **超时控制**：内置超时机制，防止任务卡死
- 🛡️ **错误恢复**：支持 panic 恢复和错误处理
- 📝 **详细日志**：完整的执行日志记录

## 配置文件

创建 `config.json` 配置文件：

```json
{
  "Email": {
    "Host": "imap.gmail.com",
    "Port": 993,
    "Username": "your-email@gmail.com",
    "Password": "your-app-password"
  },
  "DB": {
    "Host": "localhost",
    "Port": 1433,
    "Username": "your-db-username",
    "Password": "your-db-password"
  },
  "Datas": [
    {
      "Subject": "日报数据",
      "Table": "daily_report"
    },
    {
      "Subject": "月报数据",
      "Table": "monthly_report"
    }
  ],
  "Time": "0 0 9 * * *"
}
```

### 配置项说明

| 配置项 | 说明 |
|-------|------|
| `Email.Host` | 邮箱 IMAP 服务器地址 |
| `Email.Port` | IMAP 服务器端口 |
| `Email.Username` | 邮箱用户名 |
| `Email.Password` | 邮箱密码或应用密码 |
| `DB.Host` | 达梦数据库服务器地址 |
| `DB.Port` | 数据库端口 |
| `DB.Username` | 数据库用户名 |
| `DB.Password` | 数据库密码 |
| `Datas` | 数据配置数组，每项包含邮件主题和目标表名 |
| `Time` | Cron 表达式，定义任务执行时间 |

## 使用方法

1. **编译程序**
   ```bash
   # Windows
   go build -o DMEmailDataImporter.exe .

   # Linux / OSX
   go build -o DMEmailDataImporter .
   ```

2. **运行程序**
   ```bash
   # Windows
   ./DMEmailDataImporter.exe config.json

   # Linux / OSX
   ./DMEmailDataImporter config.json
   ```

3. **程序将按照配置文件中的 Time 设置定时执行任务**

## Cron 表达式说明

支持秒级精度的 Cron 表达式格式：`秒 分 时 日 月 星期`

常用示例：
- `0 0 9 * * *`：每天上午 9 点执行
- `0 */30 * * * *`：每 30 分钟执行一次
- `0 0 */2 * * *`：每 2 小时执行一次
- `0 0 9 * * 1-5`：工作日上午 9 点执行

## 工作流程

1. 程序启动后加载配置文件
2. 根据 Cron 表达式创建定时任务
3. 定时任务触发时：
   - 遍历配置中的每个数据项
   - 连接邮箱获取指定主题的邮件附件
   - 解析 Excel 附件中的数据
   - 将数据批量插入到对应的数据库表中
4. 记录详细的执行日志

## 注意事项

- 确保邮箱已开启 IMAP 服务
- Gmail 等邮箱建议使用应用专用密码而非账户密码
- 确保达梦数据库连接正常且目标表已存在
- Excel 文件应包含表头，数据从第二行开始
- 程序会跳过处理失败的附件，继续处理其他数据

## 系统要求

- Go 1.19 或更高版本
- 达梦数据库 7.0 或更高版本
- 网络连接（用于邮箱和数据库访问）

## 错误处理

程序内置多层错误处理机制：
- 任务级别的 panic 恢复
- 单个配置项处理失败不影响其他项
- 详细的错误日志记录
- 超时控制防止任务卡死

## 日志输出

程序会输出详细的执行日志，包括：
- 配置加载状态
- 任务执行进度
- 数据处理结果
- 错误信息和警告

通过日志可以监控程序运行状态和排查问题。
