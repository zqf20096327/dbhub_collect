# TiDB Cloud Serverless Terraform 構成

このTerraform構成は、TiDB CloudのServerless(Starter)クラスタを簡単にデプロイするためのものです。AWS上でServerlessクラスタを作成します。最新のv1beta1 APIキーに対応しています。

## 前提条件

1. **Terraform**: 
   ```bash
   # macOS
   brew tap hashicorp/tap
   brew install hashicorp/tap/terraform
   ```

2. **TiDB Cloud APIキー**: 
   - [TiDB Cloudコンソール](https://tidbcloud.com/console)にログイン
   - プロファイル設定に移動
   - APIキー（公開鍵と秘密鍵）を生成。組織レベルでもプロジェクトレベルでも問題ありません。クラスタの作成には*_Ownerの権限が必要です。

## セットアップ手順

1. **この構成をクローンまたはコピー**

2. **APIキーとプロジェクトIDの設定**
   
   サンプルファイルをコピーして認証情報を追加：
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
   
   `terraform.tfvars`を編集してAPIキーとプロジェクトIDを設定：
   プロジェクトIDは、TiDB CloudコンソールのURLから取得できます(project_id=...)

   ```hcl
   tidbcloud_public_key  = "your_public_key_here"
   tidbcloud_private_key = "your_private_key_here"
   project_id            = "your_project_id_here"
   ```

   または、環境変数を使用：
   ```bash
   export TF_VAR_tidbcloud_public_key="your_public_key"
   export TF_VAR_tidbcloud_private_key="your_private_key"
   export TF_VAR_project_id="your_project_id"
   ```

3. **Terraformの初期化**
   ```bash
   terraform init
   ```

4. **プランの確認**
   ```bash
   terraform plan
   ```

5. **構成の適用**
   ```bash
   terraform apply
   ```

## 設定オプション

`terraform.tfvars`で以下の変数をカスタマイズできます：

- `project_id`: TiDB CloudプロジェクトのID（必須）
- `cluster_name`: Serverlessクラスタの名前（デフォルト: "tidb-demo-serverless"）
- `cloud_provider`: クラウドプロバイダー - AWS（デフォルト: "AWS"）
- `region`: デプロイリージョン（デフォルト: "aws-ap-northeast-1"）
  - **リージョンフォーマット**: `{cloud_provider}-{region_code}`
  - **AWS例**: 
    - `aws-ap-northeast-1`（東京）
    - `aws-us-west-2`（オレゴン）
    - `aws-eu-central-1`（フランクフルト）
- `spending_limit_monthly`: 月額利用上限（セント単位、デフォルト: 1000 = $10）

## 出力情報

デプロイが成功すると、以下の情報が表示されます：

- `cluster_id`: 作成されたクラスタの一意のID
- `cluster_name`: クラスタの名前
- `cluster_status`: クラスタの現在のステータス
- `cluster_endpoints`: クラスタの接続文字列（機密情報）
- `project_id`: プロジェクトのID
- `region`: デプロイされたリージョン

## クラスタの管理

### クラスタ情報の表示
```bash
terraform show
```

### 接続情報の取得
```bash
terraform output -raw cluster_endpoints
```

### クラスタ構成の更新
`terraform.tfvars`の変数を編集して実行：
```bash
terraform apply
```

### クラスタの削除
```bash
terraform destroy
```

## 重要な注意事項

- プロジェクトIDはTiDB Cloudコンソールで確認してください
- 接続エンドポイントは機密情報としてマークされ、ログには表示されません
- プロバイダーは同期操作のために`sync = true`で設定されています

## セキュリティ

- 実際のAPIキーを含む`terraform.tfvars`をバージョン管理にコミットしないでください
- 本番環境では環境変数または安全なシークレット管理を使用してください

## トラブルシューティング

### エラー: "Your PoC credits is exhausted"
TiDB Cloudアカウントのクレジットが不足しています。以下の対処法があります：
- TiDB Cloudコンソールでクレジットを追加
- 既存のクラスタを削除してリソースを解放
- 課金アカウントにアップグレード

### エラー: "Invalid region"
リージョンフォーマットが正しいか確認してください：
- 正しいフォーマット: `aws-ap-northeast-1`
- 正しくないフォーマット: `ap-northeast-1`（`aws-`プレフィックスが必要）