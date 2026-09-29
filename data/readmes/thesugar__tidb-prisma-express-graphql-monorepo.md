# デプロイ関連
## 概要
- フロントエンド、バックエンドともに Cloud Run（同一のコンテナではなく別々）にデプロイ
- GitHub のワークフローでビルド前準備等→Dockerfile を使ってビルド→ Artifact registoryへ push→Cloud Run へデプロイの流れ

## 手順（最初に設定を行ったときの手順）
### Google Cloud にログイン
- Google Cloud Console にアクセスしてプロジェクトを作成。

### gcloud cli
- gcloud CLI をインストール。
- CLI の初期化:
  ```bash
  gcloud init
  ```
- プロジェクトの設定:
  ```bash
  gcloud config set project <YOUR_PROJECT_ID>
  ```

### サービスアカウント
GitHub Actions のワークフローなどで gcloud CLI を使って各種操作を行うにあたって、当該操作を行える権限（を持ったアカウント）が必要になる。
そのためにサービスアカウントを用意する。

まずはサービスアカウントの作成：

```bash
gcloud iam service-accounts create github-actions-deploy \
  --display-name "GitHub Actions Deploy"
```

サービスアカウントの key.json を作成しダウンロード（後で GitHub Secrets に登録する）:

```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions-deploy@tidb-prisma-express-graphql-monorepo.iam.gserviceaccount.com
```

必要な権限を付与する：

```bash
gcloud projects add-iam-policy-binding tidb-prisma-gql-monorepo \
  --member="serviceAccount:github-actions-deploy@tidb-prisma-gql-monorepo.iam.gserviceaccount.com" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding tidb-prisma-gql-monorepo \
  --member="serviceAccount:github-actions-deploy@tidb-prisma-gql-monorepo.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountActor"

gcloud projects add-iam-policy-binding tidb-prisma-gql-monorepo \
  --member="serviceAccount:github-actions-deploy@tidb-prisma-gql-monorepo.iam.gserviceaccount.com" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding tidb-prisma-gql-monorepo \
  --member="serviceAccount:github-actions-deploy@tidb-prisma-gql-monorepo.iam.gserviceaccount.com" \
  --role="roles/run.developer"

# いらないかも？
gcloud projects add-iam-policy-binding tidb-prisma-gql-monorepo \
  --member="serviceAccount:github-actions-deploy@tidb-prisma-gql-monorepo.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding tidb-prisma-gql-monorepo \
  --member="serviceAccount:github-actions-deploy@tidb-prisma-gql-monorepo.iam.gserviceaccount.com" \
  --role="roles/iam.serviceAccountUser"
```

### 環境変数の設定
GitHub Secrets に以下を登録する。
`ENV_FRONTEND_PROD` のように、あるファイルの中身全部をまとめて 1 つのシークレットとして登録する場合、詳細がまったくわからなくなるので、手元に `.env.production` など置いておくとよいかも。

- GCP_PROJECT_ID: GCP プロジェクト ID
- GCP_SERVICE_ACCOUNT_KEY: サービスアカウントの JSON キーファイルの内容（先ほどダウンロードした key.json）をそのまま貼り付ける
- TIDB_CA_CERT
  - Prisma で TiDB に接続するために必要。
  - TiDB の画面からダウンロードできる（Clusterの詳細画面→右上の Connect から。ただし、OS の部分で Windows を選ばないとダウンロードリンクが出てこない！）
  - <img src="https://private-user-images.githubusercontent.com/53966025/411279830-add30b7c-8381-4e8b-901c-01a2b6f09f5e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzkwNjc3NjMsIm5iZiI6MTczOTA2NzQ2MywicGF0aCI6Ii81Mzk2NjAyNS80MTEyNzk4MzAtYWRkMzBiN2MtODM4MS00ZThiLTkwMWMtMDFhMmI2ZjA5ZjVlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTAyMDklMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwMjA5VDAyMTc0M1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTUyMjllOTRiNGE2NTUwMmE2NjZkMTM5NmQzZTkzYTZhMDE3YmEzOTgxMTZiMjE0Njg4MGM0YmY5NDk5YWMzMzQmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.yftSgc7GSFT8EQizjTCfgCDnBFyeysxvruW4ZA0coxM" width="800" />

- ENV_FRONTEND_PROD: frontend で使うもの。
  - Cloud Run の環境変数の扱われ方の関係で、フロントエンドの環境変数は GitHub Secrets に以下を登録する。
  - .env ファイルに書く内容をそのまま GitHub Secrets に登録すればよい。`VITE_HOGEHOGE=hogehoge`

バックエンドは Cloud Run の環境変数（リビジョンの編集から）で登録する。もちろん、Cloud Run が作成されたあとでないと登録できないので、初回デプロイのときはたぶん環境変数は登録しないままとなるはず。

- DATABASE_URL: mysql://~~~.root:(PW)@gateway01.ap-northeast-1.prod.aws.tidbcloud.com:4000/test?sslaccept=strict&ssl_ca=/usr/local/share/ca-certificates/tidb-ca.crt
  - DB の URL は TiDB の画面から取得できるはず。

### Artifacts Registory
Artifact Registory のリポジトリも作っておく必要がある。

```bash
gcloud artifacts repositories create frontend-repo \
  --repository-format=docker \
  --location=asia-northeast1 \
  --description="Backend Docker images"

gcloud artifacts repositories create backend-repo \
  --repository-format=docker \
  --location=asia-northeast1 \
  --description="Backend Docker images"
```

### その他
- あとは GitHub Actions のワークフローや Dockerfile に関しては実際のソースコードを確認すること。
- ビルドコンテキストの指定とかでミスりがち。cp 漏れにより、「ファイルがありません」等も多い。
