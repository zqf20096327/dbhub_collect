# oceanbase-seekdb-2026

第六届 OceanBase 数据库大赛 **seekdb 赛题方向**仓库（AI 原生数据库 / 混合检索）。

> 本仓库为 **Private 私有仓库**。参赛代码不得对外公开，网络发现重复代码一律按作弊处理。

## 官方要求速记

- pyseekdb 要求 **Python 3.11+**（Linux glibc ≥ 2.28 / macOS；Windows 不支持嵌入式模式）
- 安装：`pip install -U pyseekdb`
- 两种连接模式：嵌入式 seekdb、远程服务器模式（seekdb 或 OceanBase）
- 常用依赖：`pymysql`、`numpy`、`sentence-transformers`

## 环境（WSL Ubuntu 24.04）

```bash
python3 --version        # 3.12.x
pip install -U pyseekdb
```

## 提交规范

- 提测时填写 **仓库地址 + 分支名/commit id**，前后**不要加空格**
- 不要把 Token / API Key 提交进仓库（已在 .gitignore 屏蔽 `.env`）
