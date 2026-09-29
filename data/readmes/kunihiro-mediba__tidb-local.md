# ローカルTiDB

## 概要

[TiDB](https://github.com/pingcap/tidb) をローカルで実行する例です。

### 初期投入SQL

`/docker/tidb-initializer/initdb.d` 直下およびサブディレクトリ内に配置したSQLをコンテナ起動時に自動実行します。

## 使い方

### 起動

```bash
docker compose up -d
```

### SQLクエリの実行

```bash
docker compose exec tidb-admin mysql -h tidb -P 4000 -u root test
```

### 全テーブルのCREATE文の取得

```bashbash
docker compose exec tidb-admin mysqldump -h tidb -P 4000 -u root test > create.sql
```

→ docker/tidbadmin/data ディレクトリに create.sql が作成される


### 終了

```bash
docker compose down
```
