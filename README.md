# fast_api_practice

## 1. APIの種類
- [なろう仕様書リポジトリ](https://github.com/watame/mobile_web_novel_reader)

## 2. 開発環境構築

### 環境変数の設定

開発環境をセットアップする前に、以下の環境変数を設定する必要があります。`.env` ファイルをプロジェクトのルートディレクトリに作成し、以下の内容を追加してください。

| 環境変数名          | 説明                   | ローカルでの推奨値        |
|-------------------|----------------------|-------------------------|
| `POSTGRES_NAME`   | Postgresのデータベース名 | `postgres`              |
| `POSTGRES_USER`   | Postgresのユーザー名    | `postgres`              |
| `POSTGRES_PASSWORD` | Postgresのパスワード    | `postgres`              |
| `POSTGRES_HOST`   | Postgresのホスト名     | `db`                    |
| `POSTGRES_PORT`   | Postgresのポート番号    | `5432`                  |
| `JWT_SECRET_ACCESS_KEY`  | JWTの秘密鍵(アクセストークン)   | `8ae240d39...376193c6`  |
| `JWT_SECRET_REFRESH_KEY`  | JWTの秘密鍵(リフレッシュトークン)  | `1608144..afdbd`  |
| `API_KEY` | APIのキー（複数設定する必要が出てきた場合はDBから取得するように変更すること）| `1f765fc8-05b2-b4a4-b290-0416ede7e712` |

### Makefile

|コマンド|内容|
|-----|-----|
| make build	| Dockerイメージの作成。開発用のdocker-compose.ymlを指定してビルドを行います。|
| make up | コンテナを起動。このコマンドはdocker-compose upコマンドをラップしており、プロジェクトに必要なサービスコンテナを起動します。|
| make down | コンテナを停止。これはdocker-compose downコマンドのラッパーで、起動しているコンテナを停止し、ネットワークを削除します。|
| make migration | マイグレーションファイルを自動生成。モデルに対して行われた変更を元に新しいマイグレーションファイルを作成します。|
| make upgrade | データベースに最新のマイグレーションを適用。データベースを最新のスキーマに更新します。|
| make fixtures | fixtures.jsonの中身をDBに登録<br>※DBの中身を初期化してから実施すること |
| make signature | APIにアクセスするための署名を表示 |

### Fixture
#### テストアカウント
|id| email | パスワード |
|-----|-----|-----|
| 1 | test01@example.com | pass |

### 動作確認
URL: http://localhost:8000
確認内容: Swagger UIの画面が表示されることを確認。これが表示されれば、アプリケーションが正しく起動している証拠です。