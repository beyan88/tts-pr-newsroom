# Cloudflare Pages 自動デプロイ設定マニュアル

当社の広報サイト（PoCモックアップ）をCloudflare Pagesへ自動デプロイするための手順書です。

## 概要
AI組織（調査部・営業部・デザイン部・監査役）によって自動生成されたコンテンツ（Markdown記事、画像、HTMLなど）をGitHubへプッシュすると、Cloudflare Pagesが自動でビルドおよび配信（デプロイ）を行います。

## 必要条件
- Cloudflareアカウント
- GitHubアカウント
- ローカル環境での `git` コマンド実行権限

## 設定手順

### 1. GitHubリポジトリの作成とプッシュ
1. GitHubに新しいリポジトリ（例: `tts-pr-newsroom`）を作成します。
2. ローカルの `cloudflare_pr_poc` フォルダ内で以下のコマンドを実行し、ファイルをプッシュします。
```bash
cd cloudflare_pr_poc
git init
git add .
git commit -m "feat: Initial commit for PR newsroom"
git branch -M main
git remote add origin https://github.com/[あなたのユーザー名]/tts-pr-newsroom.git
git push -u origin main
```

### 2. Cloudflare Pagesのセットアップ
1. Cloudflareのダッシュボードにログインします。
2. 左側のメニューから「Workers & Pages」 > 「概要」を選択し、「Pages プロジェクトの作成」をクリックします。
3. 「Git に接続」タブを選択し、GitHubアカウントを連携させます。
4. さきほど作成したリポジトリ（`tts-pr-newsroom`）を選択し、「セットアップの開始」をクリックします。

### 3. ビルドとデプロイの設定
- **プロジェクト名**: 任意の名前（例: `tts-pr-newsroom`）
- **プロダクションブランチ**: `main`
- **フレームワーク プリセット**: `なし`（今回はHTMLやMarkdownの静的ファイルのみのため）
- **ビルドコマンド**: 空白（ビルド不要）
- **ビルド出力ディレクトリ**: 空白、または `/`（ルートディレクトリ）

設定が完了したら、「保存してデプロイ」をクリックします。

### 4. 運用（自動化サイクル）
今後、AIスクリプトが `cloudflare_pr_poc/content/` に新しい記事（Markdown）を追加し、 `git push` を実行するだけで、**数秒から数十秒**でCloudflare上の広報サイトが全自動で更新されます。
これにより、田辺社長が一切関与することなく、安全かつ超高速なオウンドメディアの自律運用が可能となります。
