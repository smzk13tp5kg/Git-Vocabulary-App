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
        "related_terms": ["branch", "conflict", "rebase"],
    },
    {
        "id": "push",
        "name": "プッシュ (Push)",
        "category": "基本操作",
        "short_description": "ローカルの変更をリモートに送信",
        "full_description": "プッシュは、ローカルリポジトリのコミットをリモートリポジトリに送信する操作です。これにより、他の開発者と変更を共有できます。プッシュする前に、リモートの最新状態を取得（pull）することが推奨されます。",
        "examples": [
            "git push origin main でmainブランチをプッシュ",
            "git push -u origin feature でブランチを初回プッシュ",
        ],
        "related_terms": ["pull", "remote", "commit"],
    },
    {
        "id": "pull",
        "name": "プル (Pull)",
        "category": "基本操作",
        "short_description": "リモートの変更をローカルに取り込む",
        "full_description": "プルは、リモートリポジトリの変更をローカルリポジトリに取り込む操作です。fetch（取得）とmerge（統合）を同時に行います。チーム開発では、作業開始前に必ずpullして最新状態にすることが重要です。",
        "examples": [
            "git pull origin main でリモートの変更を取得",
            "git pull --rebase でリベースしながら取得",
        ],
        "related_terms": ["push", "fetch", "merge"],
    },
    {
        "id": "clone",
        "name": "クローン (Clone)",
        "category": "基本操作",
        "short_description": "リモートリポジトリを複製",
        "full_description": "クローンは、リモートリポジトリ全体をローカルにコピーする操作です。GitHubなどからプロジェクトをダウンロードして開発を始める際に使用します。履歴も含めて完全にコピーされます。",
        "examples": [
            "git clone https://github.com/user/repo.git",
            "git clone git@github.com:user/repo.git でSSH経由でクローン",
        ],
        "related_terms": ["repository", "remote", "fetch"],
    },
    {
        "id": "staging",
        "name": "ステージング (Staging)",
        "category": "基本概念",
        "short_description": "コミット対象を準備するエリア",
        "full_description": "ステージングエリア（インデックス）は、次のコミットに含める変更を準備する場所です。git addコマンドでファイルをステージングし、git commitで実際にコミットします。この仕組みにより、変更の一部だけをコミットすることができます。",
        "examples": [
            "git add file.txt で特定のファイルをステージング",
            "git add . ですべての変更をステージング",
            "git reset HEAD file.txt でステージングを取り消し",
        ],
        "related_terms": ["commit", "add", "status"],
    },
    {
        "id": "conflict",
        "name": "コンフリクト (Conflict)",
        "category": "トラブルシューティング",
        "short_description": "変更が競合している状態",
        "full_description": "コンフリクトは、同じファイルの同じ箇所を異なる方法で変更した際に発生します。Gitが自動的にマージできない場合、手動で解決する必要があります。コンフリクトマーカー（<<<<<<<, =======, >>>>>>>）が挿入されるので、どちらの変更を採用するか決定します。",
        "examples": [
            "コンフリクトマーカーを確認",
            "必要な変更を残して不要な部分を削除",
            "git add で解決済みをマーク",
            "git commit でマージを完了",
        ],
        "related_terms": ["merge", "rebase", "diff"],
    },
    {
        "id": "remote",
        "name": "リモート (Remote)",
        "category": "基本概念",
        "short_description": "リモートリポジトリへの参照",
        "full_description": "リモートは、ネットワーク上のリポジトリへの参照です。通常「origin」という名前が付けられます。複数のリモートを設定することも可能で、チーム開発では必須の概念です。",
        "examples": [
            "git remote -v でリモート一覧を表示",
            "git remote add origin <URL> でリモートを追加",
            "git remote rename old new で名前変更",
        ],
        "related_terms": ["push", "pull", "clone"],
    },
    {
        "id": "fetch",
        "name": "フェッチ (Fetch)",
        "category": "基本操作",
        "short_description": "リモートの情報を取得（マージはしない）",
        "full_description": "フェッチは、リモートリポジトリの最新情報を取得しますが、ローカルのブランチには自動的にマージしません。pullと異なり、安全に確認してからマージできます。",
        "examples": [
            "git fetch origin でリモートの情報を取得",
            "git fetch --all ですべてのリモートから取得",
        ],
        "related_terms": ["pull", "remote", "merge"],
    },
    {
        "id": "rebase",
        "name": "リベース (Rebase)",
        "category": "応用操作",
        "short_description": "コミット履歴を整理",
        "full_description": "リベースは、コミット履歴を別のベース上に付け替える操作です。mergeと異なり、履歴を一直線に保つことができます。ただし、既に共有されているコミットには使用すべきではありません。",
        "examples": [
            "git rebase main で現在のブランチをmainの最新に付け替え",
            "git rebase -i HEAD~3 で対話的にコミットを整理",
        ],
        "related_terms": ["merge", "commit", "interactive"],
    },
    {
        "id": "stash",
        "name": "スタッシュ (Stash)",
        "category": "応用操作",
        "short_description": "作業中の変更を一時退避",
        "full_description": "スタッシュは、コミットせずに作業中の変更を一時的に退避させる機能です。ブランチを切り替える必要があるが、まだコミットしたくない場合に便利です。",
        "examples": [
            "git stash で変更を退避",
            "git stash pop で退避した変更を復元",
            "git stash list で退避一覧を表示",
        ],
        "related_terms": ["commit", "checkout", "branch"],
    },
    {
        "id": "tag",
        "name": "タグ (Tag)",
        "category": "応用操作",
        "short_description": "特定のコミットに印をつける",
        "full_description": "タグは、特定のコミットに名前をつけて記録する機能です。主にリリースバージョンを記録するために使用されます（v1.0.0など）。軽量タグと注釈付きタグの2種類があります。",
        "examples": [
            "git tag v1.0.0 で軽量タグを作成",
            'git tag -a v1.0.0 -m "Release 1.0" で注釈付きタグ',
            "git push origin v1.0.0 でタグをプッシュ",
        ],
        "related_terms": ["commit", "release", "version"],
    },
    {
        "id": "checkout",
        "name": "チェックアウト (Checkout)",
        "category": "基本操作",
        "short_description": "ブランチやコミットを切り替える",
        "full_description": "チェックアウトは、作業するブランチを切り替えたり、過去のコミットの状態を確認したりする操作です。Git 2.23以降では、switch（ブランチ切り替え）とrestore（ファイル復元）に分割されました。",
        "examples": [
            "git checkout main でmainブランチに切り替え",
            "git checkout -b new-branch で新ブランチ作成と切り替え",
            "git checkout <commit-id> で特定のコミットを確認",
        ],
        "related_terms": ["branch", "switch", "restore"],
    },
]

CATEGORIES = ["基本概念", "基本操作", "応用操作", "トラブルシューティング"]


# ==============================
# 学習ノート（Supabase Learningnotice）
# ==============================
def save_learning_note_to_supabase(note_text: str) -> None:
    """Learningnotice テーブルにノートを1件追加"""
    supabase.ta
