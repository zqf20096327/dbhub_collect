# TiDB CRUD Demo

本專案是一個使用 Go 語言，並透過 **`sqlx`** 與 **`xo`** 整合的 **90% 自動生成 + 10% 手寫混合架構**，連線至 TiDB 資料庫進行 `Product` (商品) 資料 CRUD 操作的 HTTP REST API Demo。

本專案採用了模組化分層架構（Modular Tiered Architecture）進行設計，結合了自動生成程式碼的高效性與手寫 SQL 的靈活性。

## 架構特色

* **90% 自動生成**：利用 `xo` 讀取資料庫 Schema 自動生成基礎的 `Product` 結構體與資料庫操作（`Insert`、`Get`、`Update`、`Delete`）。
* **10% 手寫混合**：在 `dao` 層中，針對需要自訂排序或複雜條件的查詢（例如商品列表的 `List`），直接使用 `sqlx` 的 `SelectContext` 搭配自訂 SQL，享受高效的 Struct 映射。
* **分層設計**：`cmd/server` (入口) -> `routers` (路由) -> `handler` (控制器) -> `dao` (資料存取層) -> `models` (資料模型)。

## 專案結構

```text
tidb-crud-demo/
  ├── cmd/
  │   └── server/
  │       └── main.go       # 入口：加載配置、連接 TiDB、初始化資料庫、啟動 Server
  ├── conf/
  │   └── config.go         # 設定檔加載（Viper，巢狀結構）
  ├── config.yaml           # TiDB 連線與伺服器設定檔
  ├── schema.sql            # 資料庫結構定義檔，供 xo 自動生成程式碼使用
  ├── models/
  │   ├── db.xo.go          # xo 自動生成的資料庫共用邏輯與設定
  │   └── product.xo.go     # xo 自動生成的 Product 結構與基礎 CRUD 方法
  ├── dao/
  │   └── product.go        # 資料存取層（結合 xo 自動生成方法與 sqlx 手寫 List 查詢）
  ├── handler/
  │   └── product.go        # HTTP 控制器（JSON 解碼安全防護、錯誤處理與 Context 傳遞）
  ├── routers/
  │   └── router.go         # 路由定義（Go 1.22+ 原生 Mux）
  ├── go.mod                # Go Module 描述檔
  ├── test.ps1              # 自動化 API 驗證腳本
  └── README.md             # 本說明文件
```

## 系統需求

- Go 1.22 或以上版本
- 執行中的 TiDB 實例 (亦可使用原生 MySQL 替代)
- `xo` (選用，僅在需要重新生成 models 時使用)

## 自動生成程式碼指令 (xo)

本專案的 `models` 是透過 `xo` 從資料庫的 Schema 生成的。若需修改欄位，可在更新資料庫或 `schema.sql` 後，使用類似下方的指令重新生成：

```bash
xo schema mysql://root:@127.0.0.1:4000/test?parseTime=true -o models --pkg models
```

## 安裝與設定

1. 確保已開啟 TiDB 服務，並建立好對應的資料庫。
2. 啟動時程式會根據 `schema.sql` 自動建立 `products` 資料表（AutoMigrate）。
3. 檢查 `config.yaml` 內之資料庫連線 DSN (預設為 `root:@tcp(127.0.0.1:4000)/test?parseTime=true&charset=utf8mb4`)。

## 啟動服務

於專案根目錄下執行：

```bash
go run cmd/server/main.go
```

## 測試驗證

啟動服務後，可使用專案根目錄下的 PowerShell 腳本來驗證 API 端點的完整生命週期（Create, Read List, Read Single, Update, Delete）：

```powershell
powershell -ExecutionPolicy Bypass -File ./test.ps1
```
