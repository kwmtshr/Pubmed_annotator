# PubMed Annotator

## 概要
- PubMed API から論文要旨（abstract）を取得し、
- OpenAI API で要約・構造化した結果を CSV に書き出します。

## 構成
- `pubmed_client/`：コアモジュール
- `scripts/run_pubmed.py`：CLI エントリポイント
- `tests/`：pytest テスト
- `Dockerfile`：Docker イメージ定義

## セットアップ

1. リポジトリをクローン  
   ```bash
   git clone <repo_url>
   cd project
