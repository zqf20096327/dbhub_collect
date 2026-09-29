# Yoru Archive

> A membership-based ACG metadata, rating, and collection web application built with Supabase, PostgreSQL, and GitHub Pages.  
> 使用 Supabase、PostgreSQL 與 GitHub Pages 建構的會員制 ACG metadata、評分與收藏 Web 應用程式。

[繁體中文](#繁體中文) | [English](#english)

- **Live Site / 線上網站:** https://linyize1111.github.io/acg-portal/
- **Repository / 原始碼:** https://github.com/linyize1111/yoru-archive

> [!IMPORTANT]
> This source code is published for portfolio and reference purposes only.  
> It does not constitute a software license grant.
>
> 本專案原始碼僅供作品集展示與技術參考，並不代表授予任何軟體使用授權。

---

# 繁體中文

## 專案簡介

Yoru Archive 是一套私人會員制的 ACG metadata、評分與收藏 Web 應用程式。

系統用於記錄作品編號、標題、作者、標籤、評分、收藏與討論內容，但不託管作品媒體、不提供下載，也不公開來源連結。

本專案的公開儲存庫是經過整理與去敏感化的作品集版本。

正式環境使用的機密資訊、原始營運資料、資料庫備份與內部管理內容均不包含在此儲存庫中。

## 主要功能

- N／JM 目錄編號管理
- 依作品編號、標題、作者或標籤搜尋
- `-5` 至 `+5` 評分機制
- 收藏、已觀看與待觀看清單
- 作品評論與單層回覆
- Bayesian 排行榜
- 隨機作品探索
- 遊戲評鑑模組
- 會員申請與人工審核
- 可選用定時、限額的自動審核機制

> [!NOTE]
> Yoru Archive 是 metadata 與收藏管理工具，不是下載或內容散布工具。  
> 公開網站不顯示作品媒體、來源 URL 或下載連結。

## 工程實作重點

### 後端與權限控制

- Supabase／PostgreSQL 後端
- PostgreSQL Row Level Security
- RPC-based authorization
- 人工會員審核流程
- 明確定義的會員安全資料投影
- 伺服器端 UGC 驗證
- 將瀏覽器與前端視為不受信任環境

### 應用程式安全

- Content Security Policy 強化
- Stored XSS 執行階段測試
- Authenticated authorization 測試矩陣
- 跨使用者 IDOR 測試
- Privilege escalation 測試
- UGC 驗證繞過測試
- 匿名使用者與待審核會員權限測試

### 一致性與可靠性

- 具備並行安全性的伺服器端速率限制
- 使用 PostgreSQL advisory transaction locks 處理必要的並行控制
- 可重現的資料庫 migration chain
- Fail-closed 發布流程
- AES-GCM 加密備份
- 備份還原演練
- GitHub Pages 自動化部署

> [!CAUTION]
> 上述項目代表專案已實作的安全控制與測試，不代表系統「無法遭受攻擊」或「絕對安全」。

## 安全設計原則

Yoru Archive 將瀏覽器視為不受信任的執行環境。

前端權限檢查僅用於改善使用者體驗，實際授權則由 PostgreSQL Row Level Security 與 RPC 層負責執行。

安全測試涵蓋：

- 匿名存取
- 待審核會員存取
- 跨使用者 IDOR
- 權限提升
- Stored XSS runtime regression
- UGC 驗證繞過
- Rate-limit concurrency
- 備份與還原驗證

更多資訊：

- [Architecture Overview](docs/ARCHITECTURE-OVERVIEW.md)
- [Security Approach](docs/SECURITY-APPROACH.md)
- [Testing Overview](docs/TESTING-OVERVIEW.md)

## 公開版本範圍

公開網站與此儲存庫遵循以下範圍限制：

- 會員制 metadata 管理工具
- 不提供作品媒體
- 不提供下載
- 不公開來源連結
- 使用者原則上須經會員審核
- 僅能在預先排程且設有名額上限的期間啟用自動審核
- 不包含正式環境的原始營運資料
- 不包含服務端機密憑證
- 不包含私人管理或審核資料

## 技術堆疊

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Supabase
- PostgreSQL
- Supabase Auth
- PostgreSQL Row Level Security
- PostgreSQL RPC

### Security and Testing

- Playwright
- Python test utilities
- Content Security Policy
- Authorization and IDOR regression tests
- Runtime stored-XSS tests

### Deployment and Operations

- GitHub Pages
- PowerShell release tooling
- Versioned SQL migrations
- AES-GCM encrypted backups

## 系統架構

```text
[Browser]
    |
    | HTTPS
    v
[GitHub Pages]
Static HTML / CSS / JavaScript
    |
    | HTTPS / WSS
    | Publishable or anonymous key only
    v
[Supabase Auth + PostgreSQL]
Row Level Security + RPC authorization
```

瀏覽器端只會使用 Supabase publishable／anonymous key。

任何具高權限的 service credentials、資料庫管理憑證或其他機密資訊，都不應放入前端程式碼或提交至此儲存庫。

## 前端快照

此儲存庫包含經過去敏感化處理的靜態前端版本。

### 本機啟動

1. 複製前端設定範例：

   ```bash
   cp frontend/config.example.js frontend/config.js
   ```

2. 編輯 `frontend/config.js`，填入自己的：

   - Supabase URL
   - Supabase publishable／anonymous key

3. 使用任一靜態檔案伺服器啟動 `frontend/` 目錄。

   例如使用 Python：

   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

4. 在瀏覽器開啟：

   ```text
   http://localhost:8080
   ```

> [!WARNING]
> 請勿將 Supabase service-role key、資料庫密碼或其他高權限憑證放入 `frontend/config.js`。

## 文件

| 文件 | 說明 |
| --- | --- |
| [Architecture Overview](docs/ARCHITECTURE-OVERVIEW.md) | 系統架構與主要產品介面 |
| [Security Approach](docs/SECURITY-APPROACH.md) | 權限邊界與安全設計 |
| [Testing Overview](docs/TESTING-OVERVIEW.md) | 安全與回歸測試策略 |
| [Portfolio](docs/PORTFOLIO.md) | 中英文履歷與作品集摘要 |
| [Changelog](CHANGELOG.md) | 版本變更紀錄 |

## 作品集摘要

Yoru Archive 展示了以下工程能力：

- 使用 Supabase／PostgreSQL 建立 RLS 與 RPC 權限模型
- 實作會員審核、metadata 搜尋、評分、收藏、評論與排行榜
- 建立 authenticated IDOR 與 privilege-escalation regression tests
- 使用 Playwright 執行 stored-XSS runtime testing
- 使用 PostgreSQL advisory transaction locking 解決並行速率限制問題
- 建立加密備份、還原演練與 fail-closed release automation

完整內容請參閱 [Portfolio](docs/PORTFOLIO.md)。

## 授權與使用限制

本專案原始碼僅供：

- 作品集展示
- 技術研究
- 架構參考
- 安全設計討論

除非專案擁有者另行提供明確的書面授權，否則不得將此儲存庫視為已取得複製、修改、散布、部署或商業使用的軟體授權。

---

# English

## About the Project

Yoru Archive is a private, membership-based ACG metadata, rating, and collection web application.

It is designed for recording catalog IDs, titles, authors, tags, ratings, collections, and discussions. It does not host work media, provide downloads, or expose source links.

This public repository is a sanitized portfolio snapshot. Production secrets, raw operational datasets, database backups, and private moderation materials are not included.

## Core Features

- N / JM catalog ID management
- Search by catalog code, title, author, or tag
- Rating system from `-5` to `+5`
- Favorites, watched, and watchlist collections
- Reviews with one-level replies
- Bayesian leaderboard
- Random discovery
- Game review module
- Manual membership approval
- Optional time-boxed and capacity-limited automatic approval

> [!NOTE]
> Yoru Archive is a metadata and collection management tool.  
> It is not a download or content-distribution service. The public site does not display work media, source URLs, or download links.

## Engineering Highlights

### Backend and Authorization

- Supabase / PostgreSQL backend
- PostgreSQL Row Level Security
- RPC-based authorization
- Manual membership approval
- Explicit member-safe data projections
- Server-side UGC validation
- Untrusted-browser security model

### Application Security

- Content Security Policy hardening
- Runtime stored-XSS testing
- Authenticated authorization test matrix
- Cross-user IDOR testing
- Privilege-escalation testing
- UGC validation bypass testing
- Anonymous and pending-member access testing

### Reliability and Consistency

- Concurrency-safe server-side rate limiting
- PostgreSQL advisory transaction locking where required
- Reproducible database migration chain
- Fail-closed release pipeline
- AES-GCM encrypted backups
- Restore drills
- GitHub Pages deployment

> [!CAUTION]
> These are implemented controls and tests. They are not a claim that the application is invulnerable or completely secure.

## Security Model

Yoru Archive treats the browser as an untrusted environment.

Frontend authorization checks are used only for user experience. Actual authorization is enforced through PostgreSQL Row Level Security and RPC functions.

Security testing covers:

- Anonymous access
- Pending-member access
- Cross-user IDOR
- Privilege escalation
- Stored-XSS runtime regression
- UGC validation bypass
- Rate-limit concurrency
- Backup and restore verification

For more information, see:

- [Architecture Overview](docs/ARCHITECTURE-OVERVIEW.md)
- [Security Approach](docs/SECURITY-APPROACH.md)
- [Testing Overview](docs/TESTING-OVERVIEW.md)

## Public Repository Scope

The public site and repository follow these scope restrictions:

- Membership-based metadata management
- No hosted work media
- No downloads
- No exposed source links
- Membership approval is normally required
- Automatic approval may only be enabled during scheduled, capacity-limited windows
- No raw production datasets
- No privileged server credentials
- No private moderation or administrative material

## Technology Stack

### Frontend

- HTML
- CSS
- JavaScript

### Backend

- Supabase
- PostgreSQL
- Supabase Auth
- PostgreSQL Row Level Security
- PostgreSQL RPC

### Security and Testing

- Playwright
- Python test utilities
- Content Security Policy
- Authorization and IDOR regression tests
- Runtime stored-XSS tests

### Deployment and Operations

- GitHub Pages
- PowerShell release tooling
- Versioned SQL migrations
- AES-GCM encrypted backups

## Architecture

```text
[Browser]
    |
    | HTTPS
    v
[GitHub Pages]
Static HTML / CSS / JavaScript
    |
    | HTTPS / WSS
    | Publishable or anonymous key only
    v
[Supabase Auth + PostgreSQL]
Row Level Security + RPC authorization
```

The browser uses only the Supabase publishable or anonymous key.

Privileged service credentials, database administration credentials, and other secrets must never be included in frontend code or committed to this repository.

## Frontend Snapshot

This repository contains a sanitized snapshot of the static frontend.

### Local Setup

1. Copy the frontend configuration example:

   ```bash
   cp frontend/config.example.js frontend/config.js
   ```

2. Edit `frontend/config.js` and provide your own:

   - Supabase URL
   - Supabase publishable or anonymous key

3. Serve the `frontend/` directory with any static file server.

   For example, using Python:

   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

4. Open the following address:

   ```text
   http://localhost:8080
   ```

> [!WARNING]
> Never place a Supabase service-role key, database password, or any other privileged credential in `frontend/config.js`.

## Documentation

| Document | Description |
| --- | --- |
| [Architecture Overview](docs/ARCHITECTURE-OVERVIEW.md) | System architecture and product surfaces |
| [Security Approach](docs/SECURITY-APPROACH.md) | Authorization boundaries and security design |
| [Testing Overview](docs/TESTING-OVERVIEW.md) | Security and regression testing strategy |
| [Portfolio](docs/PORTFOLIO.md) | Traditional Chinese and English portfolio summary |
| [Changelog](CHANGELOG.md) | Version history and notable changes |

## Portfolio Summary

Yoru Archive demonstrates experience in:

- Designing Supabase / PostgreSQL RLS and RPC authorization models
- Implementing membership approval, metadata search, ratings, collections, reviews, and ranking
- Building authenticated IDOR and privilege-escalation regression tests
- Running stored-XSS runtime tests with Playwright
- Resolving concurrency issues with PostgreSQL advisory transaction locking
- Building encrypted backups, restore drills, and fail-closed release automation

See [Portfolio](docs/PORTFOLIO.md) for the complete resume-oriented summary.

## License and Usage

The source code in this repository is published only for:

- Portfolio presentation
- Technical study
- Architecture reference
- Security design discussion

Unless the repository owner provides an explicit written license, this repository must not be interpreted as granting permission to copy, modify, distribute, deploy, or commercially use the software.
