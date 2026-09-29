# 🎬 基于 [mdcx 项目](https://github.com/sqzw-x/mdcx) 的刮削数据处理方案

## 📌 项目功能概述

- **功能 1**：将刮削后的 `.nfo` 文件中的元数据写入 SQLite 数据库，同时将海报等图片上传至 GitHub 仓库。
- **功能 2**：从数据库读取番号信息进行快速刮削，效率更高。
---

## 📁 文件结构示例

```text
演员/
└── 番号 演员/
    ├── 番号-fanart.jpg
    ├── 番号-poster.jpg
    ├── 番号-thumb.jpg
    ├── 番号.mp4
    └── 番号.nfo
```

> 当前已处理 166 个文件，数据库大小为 732KB。预计处理 10,000 个文件约为 43MB，体积不算大。仅遇到 1 个特殊字符写入报错问题。
> 库里面有一个测试的sqlite文件可以直接使用，查看数据库中的内容推荐使用DB Browser for SQLite
---

## ⚙️ 使用方法

### 1️⃣ `main_text_to_sql`

将刮削后的文件夹（如 `C:\test\JAV_output`）中的数据写入 SQLite 数据库：

- 每个 `.nfo` 文件中的 tag 会作为数据库字段。
- 冲突字段自动添加后缀（如 `set_pri`）。
- 图片（poster、thumb、fanart）会进行哈希处理并上传至 GitHub。

### 2️⃣ `main_scrapy`

从数据库中匹配番号进行刮削：

- 输入对象为视频文件夹，支持子文件夹。
- 视频文件仅支持 Windows 的硬链接。
- 当 fanart 与 thumb 图片相同时，可选择复制或使用硬链接。

---

## 🧾 配置文件说明（`config.ini`）

### `[text_process]`

| 参数  | 说明  |
| --- | --- |
| `sql_suffix` | 冲突字段添加后缀，如 `set_pri` |
| `sql_add` | 写入数据库时添加的字段，读取时会删除 |
| `sort_op` | 是否启用参考排序（默认关闭） |
| `sort_comfren` | 启用排序时的字段顺序参考列表 |

---

### `[proxies]`

```ini
http = http://127.0.0.1:10808
https = http://127.0.0.1:10808
```

---

### `[github_info]`

| 参数  | 说明  |
| --- | --- |
| `use_token` | 是否使用 GitHub Token（上传/下载需要） |
| `repo` | GitHub 仓库路径，如 `用户名/仓库` |
| `branch` | 分支名，如 `main` |
| `token` | GitHub Token，如 `ghp_XXXXX` |
| `max_try_upload` | 上传图片最大尝试次数 |

---

### `[sql_info]`

| 参数  | 说明  |
| --- | --- |
| `db_file` | 数据库文件路径 |
| `table_name` | 表名  |
| `main_key` | 主键字段，必须唯一且不能为空 |
| `update_op` | 是否更新已有数据（`False` 为跳过） |

---

### `[scripy_op]`

| 参数  | 说明  |
| --- | --- |
| `use_hardlink` | fanart 与 poster 相同时是否使用硬链接（`False` 为复制） |

---

### `[folder_name]`

```ini
folder_name = JAV_output
```

> 建议保持默认，不建议修改。
>
> 注：作者是自学的，代码太烂望见谅！！！
