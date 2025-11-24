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
# カスタムCSS
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

/* ▼▼ 用語選択ボタン（中央カラム）のカスタムスタイル ▼▼ */
.term-button-container .stButton {
    width: 100%;
}

.term-button-container .stButton > button {
    position: relative;
    width: 100%;
    padding: 0.9rem 1.1rem;
    border-radius: 12px;
    border: 1px solid #CCFFFF;   /* 枠線：アニメーションカラーに合わせる */
    background-color: #FFFFFF;    /* ベースカラー */
    color: #111827;
    text-align: left;
    font-size: 0.90rem;
    font-weight: 500;
    overflow: hidden;             /* アニメーションをボタン内に閉じ込める */
}

/* ボタン内テキストを前面に出す */
.term-button-container .stButton > button > div {
    position: relative;
    z-index: 2;
}

/* ホバーアニメーション用レイヤー */
.term-button-container .stButton > button::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #CCFFFF;          /* アニメーションカラー */
    transform: translateX(-96%);
    transition: transform .5s ease-in-out;
    z-index: 1;
}

/* ホバー時に左からスライドしてくる */
.term-button-container .stButton > button:hover::before {
    transform: translateX(0%);
}

/* ホバー時のテキスト色（少し濃く） */
.term-button-container .stButton > button:hover {
    color: #111827;
}
</style>
""",
    unsafe_allow_html=True,
)

def inject_flat_button_css():
    st.markdown(
        """
<style>
/* クイズ系アクションボタン共通スタイル */
/* 通常ボタン(st.button) と フォーム送信ボタン(st.form_submit_button) の両方を対象にする */
.stButton > button,
.stFormSubmitButton > button {
  font-size: 1.6rem;
  font-weight: 700;
  line-height: 1.5;
  position: relative;
  display: inline-block;
  padding: 1.5rem 6rem;
  cursor: pointer;
  user-select: none;
  transition: all 0.3s;
  text-align: center;
  vertical-align: middle;
  text-decoration: none;
  letter-spacing: 0.1em;
  color: #fff;
  border-radius: 0;
  background: #000;
  border: none;
  overflow: hidden;
}

/* ラベルを前面に出す（アニメレイヤーより上） */
.stButton > button > div,
.stFormSubmitButton > button > div {
  position: relative;
  z-index: 1;
}

/* ▼▼ ここが a.btn-flat の書き換え版 ▼▼ */
.stButton > button::before,
.stFormSubmitButton > button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: all .5s ease-in-out;
  transform: translateX(-96%);
  background: #eb6877;
  z-index: 0;
}

.stButton > button:hover::before,
.stFormSubmitButton > button:hover::before {
  transform: translateX(0%);
}
</style>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
<style>
/* ▼▼ 辞書モード用：フラットボタン（AliceBlue / Azure） ▼▼ */

.term-button-container .stButton > button {
    position: relative;
    width: 100%;
    padding: 0.9rem 1.1rem;
    border-radius: 12px;
    border: 1px solid #F0FFFF;       /* Azure */
    background-color: #F0F8FF;       /* AliceBlue */
    color: #111827;
    text-align: left;
    font-size: 0.90rem;
    font-weight: 500;
    overflow: hidden;
}

/* テキスト前面 */
.term-button-container .stButton > button > div {
    position: relative;
    z-index: 2;
}

/* スライドアニメ：Azure */
.term-button-container .stButton > button::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: #F0FFFF;             /* Azure */
    transform: translateX(-96%);
    transition: transform .5s ease-in-out;
    z-index: 1;
}

/* Hover時：スライドイン */
.term-button-container .stButton > button:hover::before {
    transform: translateX(0%);
}

/* Hover時テキスト色 */
.term-button-container .stButton > button:hover {
    color: #111827;
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
# 学習ノート（Supabase learning_notes）
# ==============================
def save_learning_note_to_supabase(note_text: str) -> None:
    """learning_notes テーブルにノートを1件追加"""
    supabase.table("learning_notes").insert({"note_text": note_text}).execute()


def load_learning_notes_from_supabase(limit: int = 50) -> List[Dict]:
    """learning_notes テーブルからノート履歴を取得（新しい順）"""
    res = (
        supabase.table("learning_notes")
        .select("*")
        .order("id", desc=True)  # id 降順で新しい順
        .limit(limit)
        .execute()
    )
    return res.data or []

# ==============================
# クイズ問題（Supabase git_quiz_questions）
# ==============================
def load_quiz_questions_from_supabase(limit: int = 5) -> List[Dict]:
    """git_quiz_questions からクイズ問題を取得"""
    res = (
        supabase.table("git_quiz_questions")
        .select("*")
        .limit(limit)
        .execute()
    )
    return res.data or []


def insert_quiz_question_to_supabase(
    question_text: str,
    choice_1: str,
    choice_2: str,
    choice_3: str,
    choice_4: str,
    correct_choice: int,
    explanation: str,
) -> None:
    """git_quiz_questions にクイズ問題を追加"""
    supabase.table("git_quiz_questions").insert(
        {
            "question_text": question_text,
            "choice_1": choice_1,
            "choice_2": choice_2,
            "choice_3": choice_3,
            "choice_4": choice_4,
            "correct_choice": correct_choice,
            "explanation": explanation,
        }
    ).execute()

# ==============================
# セッション状態
# ==============================
if "selected_term_id" not in st.session_state:
    st.session_state.selected_term_id = "repository"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "learning_note_input" not in st.session_state:
    st.session_state.learning_note_input = ""

# ==============================
# タイトル & サマリ
# ==============================
st.title("📚 Git用語ミニ辞典")

top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.markdown(
        "Git の基本用語を日本語でざっと確認できるミニ辞典です。"
        "検索・カテゴリフィルタ・使用例・関連用語をひとつの画面で確認できます。"
    )

with top_col2:
    total_terms = len(TERMS)
    total_categories = len(set(t["category"] for t in TERMS))
    st.metric("登録用語数", total_terms)
    st.metric("カテゴリ数", total_categories)

st.info("💡 左のサイドバーから表示モードやフィルタ条件を変更できます。")

# ==============================
# サイドバー
# ==============================
with st.sidebar:
    st.subheader("⚙ 表示設定")

    mode = st.radio(
        "学習モード",
        options=["辞書モード", "クイズに挑戦", "クイズ登録"],
        index=0,
    )

    category_filter = st.selectbox(
        "カテゴリフィルタ",
        options=["すべて"] + CATEGORIES,
        index=0,
    )

    include_advanced = st.checkbox("応用操作・トラブルシューティングも含める", value=True)

    max_items = st.slider("最大表示件数", min_value=5, max_value=50, value=20, step=5)

# ==============================
# 辞書モード
# ==============================
if mode == "辞書モード":
    # 検索バー
    search_col1, search_col2 = st.columns([3, 1])

    with search_col1:
        search_query = st.text_input(
            "🔍 用語を検索...",
            value=st.session_state.search_query,
            placeholder="用語名や一言説明で検索",
        )
        st.session_state.search_query = search_query

    with search_col2:
        st.caption("※ 大文字小文字は区別されません")

    # フィルタリング
    filtered_terms = TERMS

    if category_filter != "すべて":
        filtered_terms = [t for t in filtered_terms if t["category"] == category_filter]

    if not include_advanced:
        filtered_terms = [
            t for t in filtered_terms
            if t["category"] not in ("応用操作", "トラブルシューティング")
        ]

    if search_query:
        q = search_query.lower()
        filtered_terms = [
            t for t in filtered_terms
            if q in t["name"].lower() or q in t["short_description"].lower()
        ]

    filtered_terms = filtered_terms[:max_items]

    # タブ
    tab_dict, tab_table, tab_memo = st.tabs(["📋 辞書ビュー", "📊 一覧表", "📝 ノート"])

    # --- 辞書ビュー ---
    # --- 辞書ビュー ---
    with tab_dict:
        col_left, col_mid, col_right = st.columns([1.4, 1.2, 2])

        # 左カラム：概要
        with col_left:
            st.subheader("🌿 Gitとは")
            st.markdown(
                """
Gitは、ソースコードのバージョン管理システムです。
ファイルの変更履歴を記録し、過去の状態にいつでも戻ることができます。
"""
            )
            with st.expander("📖 なぜGitが必要？", expanded=True):
                st.markdown(
                    """
- 変更履歴を完全に記録できる  
- いつでも過去の状態に戻せる  
- 複数人で同時に開発できる  
- 実験的な開発を安全に実施できる  
"""
                )

        # 中央カラム：用語一覧（★ここにスタイル適用★）
        with col_mid:
            st.subheader("📋 用語一覧")
            st.caption(f"{len(filtered_terms)} 件ヒット")

            list_mode = st.radio(
                "表示順",
                options=["カテゴリ別", "名前順"],
                horizontal=True,
                key="list_mode",
            )

            # ▼ カスタムスタイル用のコンテナで囲む ▼
            st.markdown(
                '<div class="term-button-container">',
                unsafe_allow_html=True,
            )

            if list_mode == "名前順":
                terms_for_view = sorted(filtered_terms, key=lambda t: t["name"])
                for term in terms_for_view:
                    if st.button(
                        f"{term['name']}：{term['short_description']}",
                        key=f"term_{term['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.selected_term_id = term["id"]
            else:
                for category in CATEGORIES:
                    cat_terms = [
                        t for t in filtered_terms if t["category"] == category
                    ]
                    if not cat_terms:
                        continue

                    st.markdown(
                        f"<div class='category-header'>{category}</div>",
                        unsafe_allow_html=True,
                    )
                    for term in cat_terms:
                        if st.button(
                            f"{term['name']}：{term['short_description']}",
                            key=f"term_{term['id']}",
                            use_container_width=True,
                        ):
                            st.session_state.selected_term_id = term["id"]
                            break

            # ▲ コンテナ終わり ▲
            st.markdown("</div>", unsafe_allow_html=True)

        # 右カラム：用語詳細
        with col_right:
            selected_term = next(
                (t for t in TERMS if t["id"] == st.session_state.selected_term_id),
                TERMS[0],
            )

            st.subheader("📖 用語詳細")
            st.markdown(
                f"<span class='tag'>📌 {selected_term['category']}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(f"### {selected_term['name']}")
            st.markdown(f"**一言説明：** {selected_term['short_description']}")

            st.markdown("---")
            st.markdown("#### 詳細説明")
            st.markdown(
                f"""
<div style="background-color: #f9fafb; padding: 1rem; border-radius: 0.5rem;">
  <p style="color: #374151; line-height: 1.75; margin: 0;">
    {selected_term['full_description']}
  </p>
</div>
""",
                unsafe_allow_html=True,
            )


    # --- 一覧表 ---
    with tab_table:
        st.subheader("📊 用語一覧（表形式）")
        table_data = [
            {
                "ID": t["id"],
                "用語": t["name"],
                "カテゴリ": t["category"],
                "一言説明": t["short_description"],
            }
            for t in filtered_terms
        ]
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

    # --- 学習ノート ---
    with tab_memo:
        st.subheader("📝 学習ノート（Supabase 保存）")

        st.markdown(
            """
Git やこの辞典を使って気づいたこと・疑問点・
社内での運用アイデアなどを自由にメモできます。  
「ノートを保存」を押すと Supabase の learning_notes テーブルに蓄積されます。
"""
        )

        new_note = st.text_area(
            "新しい学習メモを入力",
            value=st.session_state.learning_note_input,
            height=150,
        )

        if st.button("✏️ ノートを保存"):
            if new_note.strip():
                save_learning_note_to_supabase(new_note.strip())
                st.success("Supabase の learning_notes テーブルに保存しました。")
                st.session_state.learning_note_input = ""
            else:
                st.warning("テキストを入力してください。")

        st.markdown("---")
        st.markdown("#### 📚 ノート履歴（新しい順 最大50件）")

        notes = load_learning_notes_from_supabase(limit=50)
        if not notes:
            st.info("まだ learning_notes にノートがありません。最初の1件を書いてみましょう。")
        else:
            for row in notes:
                created_at = row.get("created_at")
                if created_at:
                    date_str = str(created_at).replace("T", " ").split(".")[0][:16]
                else:
                    date_str = f"ID: {row.get('id', '?')}"
                st.markdown(f"**{date_str}**  \n{row.get('note_text', '')}")
                st.markdown("---")

# ==============================
# クイズに挑戦モード
# ==============================
elif mode == "クイズに挑戦":
    inject_flat_button_css()  # ★ここを追加
    st.title("🧩 Git クイズに挑戦")

    questions = load_quiz_questions_from_supabase(limit=5)

    if not questions:
        st.warning("Supabase の git_quiz_questions に問題が登録されていません。")
    else:
        st.markdown("Supabase に登録された問題から、ランダムに最大5問を出題します。")

        if "quiz_answers" not in st.session_state:
            st.session_state.quiz_answers = {}

        for idx, q in enumerate(questions):
            st.markdown(f"### Q{idx + 1}. {q['question_text']}")
            options = [
                q["choice_1"],
                q["choice_2"],
                q["choice_3"],
                q["choice_4"],
            ]
            user_answer = st.radio(
                "選択肢を選んでください",
                options,
                key=f"quiz_q_{q['id']}",
            )
            st.session_state.quiz_answers[q["id"]] = user_answer
            st.write("---")

        if st.button("採点する"):
            score = 0
            results = []

            for q in questions:
                correct_index = (q.get("correct_choice") or 1) - 1
                correct_index = max(0, min(correct_index, 3))
                correct_text = [
                    q["choice_1"],
                    q["choice_2"],
                    q["choice_3"],
                    q["choice_4"],
                ][correct_index]

                user_answer = st.session_state.quiz_answers.get(q["id"])
                is_correct = (user_answer == correct_text)
                if is_correct:
                    score += 1

                results.append((q, is_correct, correct_text, user_answer))

            st.subheader(f"結果: {score} / {len(questions)} 問 正解")

            for idx, (q, is_correct, correct_text, user_answer) in enumerate(results):
                st.markdown(f"#### Q{idx + 1}. {q['question_text']}")
                if is_correct:
                    st.success(f"✔ 正解！ あなたの回答: {user_answer}")
                else:
                    st.error(
                        f"✖ 不正解… あなたの回答: {user_answer} ／ 正解: {correct_text}"
                    )
                if q.get("explanation"):
                    st.info(f"解説: {q['explanation']}")
                st.write("---")

# ==============================
# クイズ登録モード
# ==============================
elif mode == "クイズ登録":
    inject_flat_button_css()  # ★ここを追加
    st.title("🛠 Git クイズ問題の登録")

    st.markdown(
        """
git_quiz_questions テーブルにクイズ問題を登録します。  
4択問題＋正解番号＋解説を入力して「登録」ボタンを押してください。
"""
    )

    with st.form("quiz_create_form"):
        question_text = st.text_area("問題文", height=100)

        col1, col2 = st.columns(2)
        with col1:
            choice_1 = st.text_input("選択肢1")
            choice_2 = st.text_input("選択肢2")
        with col2:
            choice_3 = st.text_input("選択肢3")
            choice_4 = st.text_input("選択肢4")

        correct_choice = st.selectbox(
            "正解の選択肢番号",
            options=[1, 2, 3, 4],
            index=0,
        )

        explanation = st.text_area("解説（任意）", height=120)

        submitted = st.form_submit_button("この内容でクイズを登録")

    if submitted:
        if not question_text.strip():
            st.warning("問題文を入力してください。")
        elif not (choice_1.strip() and choice_2.strip() and choice_3.strip() and choice_4.strip()):
            st.warning("4つすべての選択肢を入力してください。")
        else:
            insert_quiz_question_to_supabase(
                question_text=question_text.strip(),
                choice_1=choice_1.strip(),
                choice_2=choice_2.strip(),
                choice_3=choice_3.strip(),
                choice_4=choice_4.strip(),
                correct_choice=int(correct_choice),
                explanation=explanation.strip(),
            )
            st.success("git_quiz_questions テーブルにクイズ問題を登録しました。")

    st.markdown("---")
    st.markdown("#### 最近登録された問題（確認用）")

    latest_questions = load_quiz_questions_from_supabase(limit=5)
    if not latest_questions:
        st.info("まだクイズ問題が登録されていません。")
    else:
        for q in latest_questions:
            st.markdown(f"- **{q['question_text']}**")








