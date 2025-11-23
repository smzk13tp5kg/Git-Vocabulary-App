import os

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
    st.error("SUPABASE_URL / SUPABASE_KEY が .env に設定されていません。")
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
    # ...（他の TERMS は元コードのまま省略）...
]

CATEGORIES = ["基本概念", "基本操作", "応用操作", "トラブルシューティング"]

# ==============================
# 学習ノート（Supabase 読み書き）
# ==============================

@st.cache_data
def load_learning_notes():
    """
    Supabase の learning_notes テーブルからノート一覧を取得
    最新順に並べて返す
    """
    res = (
        supabase.table("learning_notes")
        .select("id, note_text, created_at")
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def save_learning_note(note_text: str):
    """
    Supabase に学習ノートを1件追記
    """
    supabase.table("learning_notes").insert(
        {"note_text": note_text}
    ).execute()
    # 追記したのでキャッシュをクリア
    load_learning_notes.clear()


# ==============================
# セッション状態
# ==============================
if "selected_term_id" not in st.session_state:
    st.session_state.selected_term_id = "repository"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# ノート入力欄用のセッションキー
if "global_note_input" not in st.session_state:
    st.session_state.global_note_input = ""

# ==============================
# タイトル & メトリクス
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

    mode = st.radio("学習モード", options=["辞書モード", "クイズ準備中"], index=0)

    category_filter = st.selectbox(
        "カテゴリフィルタ",
        options=["すべて"] + CATEGORIES,
        index=0,
    )

    include_advanced = st.checkbox("応用操作・トラブルシューティングも含める", value=True)

    max_items = st.slider("最大表示件数", min_value=5, max_value=50, value=20, step=5)

    st.markdown("---")
    st.caption("このアプリについてのフィードバック（ダミー）")

    with st.form("feedback_form"):
        name = st.text_input("お名前（任意）")
        rating = st.slider("分かりやすさ（1〜5）", 1, 5, 4)
        comment = st.text_area("コメント", height=80)
        submitted = st.form_submit_button("送信")
        if submitted:
            st.success("フィードバックありがとうございます！")

# ==============================
# 検索バー
# ==============================
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

# ==============================
# 用語フィルタリング
# ==============================
filtered_terms = TERMS

# カテゴリフィルタ
if category_filter != "すべて":
    filtered_terms = [t for t in filtered_terms if t["category"] == category_filter]

# 応用・トラブルの除外
if not include_advanced:
    filtered_terms = [
        t
        for t in filtered_terms
        if t["category"] not in ("応用操作", "トラブルシューティング")
    ]

# 検索フィルタ
if search_query:
    q = search_query.lower()
    filtered_terms = [
        t
        for t in filtered_terms
        if q in t["name"].lower() or q in t["short_description"].lower()
    ]

# 件数制限
filtered_terms = filtered_terms[:max_items]

# ==============================
# タブレイアウト
# ==============================
tab_dict, tab_table, tab_memo = st.tabs(["📋 辞書ビュー", "📊 一覧表", "📝 ノート"])

# ---------- タブ1：辞書ビュー ----------
with tab_dict:
    col_left, col_mid, col_right = st.columns([1.4, 1.2, 2])

    # 左カラム：Gitとは
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

        with st.expander("👥 チーム開発での利点"):
            st.markdown(
                """
- 各自が独立して作業できる  
- 変更内容を簡単に共有できる  
- コードレビューが容易  
- 誰が何を変更したか追跡できる  
"""
            )

        with st.expander("🛡️ 安全性"):
            st.markdown(
                """
- データの完全性を保証  
- 分散型で障害に強い  
- 複数リモートでバックアップ  
- 誤った変更も簡単に復元  
"""
            )

        st.markdown("---")
        st.markdown("#### 🔄 基本的なワークフロー")
        steps = [
            "ファイルを編集",
            "変更をステージング（git add）",
            "コミット（git commit）",
            "リモートにプッシュ（git push）",
        ]
        for i, step in enumerate(steps, 1):
            st.markdown(
                f"""
<div class="workflow-step">
  <div class="step-number">{i}</div>
  <div style="font-size: 0.875rem; color: #374151; padding-top: 0.125rem;">
    {step}
  </div>
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown(
            """
<div class="info-box amber">
  <p style="margin: 0; font-size: 0.875rem; color: #92400e;">
    💡 <strong>ヒント：</strong>
    最初は add / commit / push / pull の4つだけに集中して、
    実際に手を動かしながら覚えるのがおすすめです。
  </p>
</div>
""",
            unsafe_allow_html=True,
        )

    # 中央カラム：用語一覧
    with col_mid:
        st.subheader("📋 用語一覧")
        st.caption(f"{len(filtered_terms)} 件ヒット")

        list_mode = st.radio(
            "表示順",
            options=["カテゴリ別", "名前順"],
            horizontal=True,
            key="list_mode",
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
                cat_terms = [t for t in filtered_terms if t["category"] == category]
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
        st.markdown(
            f"**一言説明：** {selected_term['short_description']}",
        )

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

        if selected_term.get("examples"):
            st.markdown("#### 💻 使用例")
            for example in selected_term["examples"]:
                st.code(example, language="bash")

        if selected_term.get("related_terms"):
            st.markdown("#### 🔗 関連用語")
            related_terms = [
                t
                for t in TERMS
                if t["id"] in selected_term.get("related_terms", [])
            ]
            for rt in related_terms:
                if st.button(
                    f"{rt['name']}：{rt['short_description']}",
                    key=f"related_{rt['id']}",
                ):
                    st.session_state.selected_term_id = rt["id"]

        st.markdown("---")
        st.info(
            "💬 「📝 ノート」タブに、学んだことや自分の言葉での説明をメモしておくと、"
            "あとから復習したり、社内向け教材のタネにできます。"
        )

# ---------- タブ2：一覧表 & ダウンロード ----------
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

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="📥 この一覧をCSVでダウンロード",
        data=csv,
        file_name="git_terms.csv",
        mime="text/csv",
    )

    st.caption("※ 絞り込み条件・検索結果に応じた内容がダウンロードされます。")

# ---------- タブ3：全体ノート ----------
with tab_memo:
    st.subheader("📝 学習ノート")

    st.markdown(
        """
Gitやこの辞典を使って気づいたこと・疑問点・社内での運用ルール案などを、
自由にメモしておくスペースです。
「保存」を押すたびに、新しいノートとしてSupabaseに記録されます。
"""
    )

    # 入力欄
    global_note = st.text_area(
        "学習メモ（1件分）",
        value=st.session_state.global_note_input,
        height=200,
        key="global_note_input",
    )

    col_save, col_dummy = st.columns([1, 3])
    with col_save:
        if st.button("💾 保存", use_container_width=True):
            if st.session_state.global_note_input.strip():
                save_learning_note(st.session_state.global_note_input.strip())
                st.success("Supabase に学習ノートを保存しました。")

                # 入力欄をクリア
                st.session_state.global_note_input = ""
            else:
                st.warning("メモが空です。何か入力してから保存してください。")

    st.markdown("---")
    st.markdown("#### 📚 保存済みノート一覧（最新順）")

    notes = load_learning_notes()
    if not notes:
        st.info("まだ保存されたノートはありません。上の入力欄から最初のメモを残してみてください。")
    else:
        for n in notes:
            st.markdown(
                f"- {n['created_at']}: {n['note_text']}"
            )
