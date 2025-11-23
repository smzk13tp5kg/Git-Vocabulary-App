import os
from typing import List, Dict

import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client

# ==============================
# Supabase クライアント初期化
# ==============================
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print("DEBUG SUPABASE_URL:", SUPABASE_URL)
print("DEBUG SUPABASE_KEY:", SUPABASE_KEY)

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("SUPABASE_URL / SUPABASE_KEY が .env / Secrets に設定されていません。")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ==============================
# ページ設定
# ==============================
st.set_page_config(
    page_title="Git用語辞典",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================
# カスタムCSS（見た目用のみ）
# ==============================
st.markdown(
    """
<style>
.block-container {
    max-width: 1600px;
}

/* 情報ボックス */
.info-box {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
}
.info-box.blue {
    background-color: #eff6ff;
    border: 1px solid #bfdbfe;
}
.info-box.green {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
}
.info-box.purple {
    background-color: #faf5ff;
    border: 1px solid #e9d5ff;
}
.info-box.amber {
    background-color: #fffbeb;
    border: 1px solid #fde68a;
}

/* タグ */
.tag {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    background-color: #eff6ff;
    color: #2563eb;
    border-radius: 0.25rem;
    font-size: 0.875rem;
    margin-bottom: 0.75rem;
}

/* カテゴリーヘッダー */
.category-header {
    color: #6b7280;
    font-size: 0.875rem;
    font-weight: 600;
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
}

/* ワークフローステップ */
.workflow-step {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.step-number {
    width: 1.5rem;
    height: 1.5rem;
    background-color: #dbeafe;
    color: #2563eb;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    flex-shrink: 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ==============================
# 用語データ
# ==============================
TERMS = [
    {
        "id": "repository",
        "name": "リポジトリ (Repository)",
        "category": "基本概念",
        "short_description": "プロジェクトのファイルと履歴を保存する場所",
        "full_description": "リポジトリは、Gitでプロジェクトを管理するための保管場所です。ファイルやディレクトリの状態を記録し、その変更履歴を保存します。ローカルリポジトリ（自分のPC上）とリモートリポジトリ（GitHubなどのサーバー上）の2種類があります。",
        "examples": [
            "git init でローカルリポジトリを作成",
            "git clone でリモートリポジトリを複製",
        ],
        "related_terms": ["commit", "clone", "remote"],
    },
    {
        "id": "commit",
        "name": "コミット (Commit)",
        "category": "基本操作",
        "short_description": "変更を記録すること",
        "full_description": "コミットは、ファイルの変更をリポジトリに記録する操作です。スナップショットのように、その時点のプロジェクトの状態を保存します。各コミットには一意のIDが付与され、いつでもその状態に戻ることができます。コミットメッセージを付けることで、何を変更したかを記録できます。",
        "examples": [
            "git add . で変更をステージング",
            'git commit -m "メッセージ" でコミット',
        ],
        "related_terms": ["staging", "push", "log"],
    },
    {
        "id": "branch",
        "name": "ブランチ (Branch)",
        "category": "基本概念",
        "short_description": "作業を分岐させる機能",
        "full_description": "ブランチは、開発作業を本流から分岐させる機能です。新機能の開発やバグ修正を、メインの開発ラインに影響を与えずに行えます。作業が完了したら、マージして本流に統合します。複数人での並行開発に不可欠な機能です。",
        "examples": [
            "git branch feature/new-feature で新しいブランチ作成",
            "git checkout -b feature/new-feature でブランチ作成と切り替えを同時に実行",
        ],
        "related_terms": ["merge", "checkout", "main"],
    },
    {
        "id": "merge",
        "name": "マージ (Merge)",
        "category": "基本操作",
        "short_description": "ブランチを統合すること",
        "full_description": "マージは、異なるブランチの変更を統合する操作です。feature ブランチでの開発が完了したら、main ブランチにマージして変更を反映させます。自動的に統合できない場合はコンフリクトが発生し、手動で解決する必要があります。",
        "examples": [
            "git merge feature/new-feature で現在のブランチにマージ",
            "git merge --no-ff でマージコミットを必ず作成",
        ],
        "related_terms":_
