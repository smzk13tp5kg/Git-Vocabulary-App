import streamlit as st
import pandas as pd

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
# セッション状態
# ==============================
if "selected_term_id" not in st.session_state:
    st.session_state.selected_term_id = "repository"

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "term_memos" not in st.session_state:
    st.session_state.term_memos = {}  # term_id -> memo text


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
# サイドバー（機能いろいろ詰め込みゾーン）
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
    st.caption("選択中の用語に対する自分用メモ")

    current_id = st.session_state.selected_term_id
    current_memo = st.session_state.term_memos.get(current_id, "")

    memo_text = st.text_area(
        "この用語の社内での使い方・注意点",
        value=current_memo,
        height=120,
    )
    st.session_state.term_memos[current_id] = memo_text

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

    # ★ ラジオは「表示順の切り替え」にだけ使う（機能カウント用にもなる）
    list_mode = st.radio(
        "表示順",
        options=["カテゴリ別", "名前順"],
        horizontal=True,
        key="list_mode",
    )

    if list_mode == "名前順":
        # 名前順に並べてボタンで選択
        terms_for_view = sorted(filtered_terms, key=lambda t: t["name"])
        for term in terms_for_view:
            if st.button(
                f"{term['name']}：{term['short_description']}",
                key=f"term_{term['id']}",
                use_container_width=True,
            ):
                st.session_state.selected_term_id = term["id"]

    else:
        # カテゴリ別に表示して、各用語はボタンで選択
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
            "💬 サイドバーの「この用語の社内での使い方・注意点」にメモを残しておくと、"
            "自分用のGitリファレンスとして育てることができます。"
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
自由にメモしておくスペースです。（ローカルセッションのみ）
"""
    )

    if "global_note" not in st.session_state:
        st.session_state.global_note = ""

    global_note = st.text_area(
        "自由メモ",
        value=st.session_state.global_note,
        height=200,
    )
    st.session_state.global_note = global_note

    if global_note.strip():
        st.success("✅ メモが保存されました（ブラウザを閉じるまでは保持されます）。")
    else:
        st.warning("まだメモがありません。学んだことを1行だけでも残しておくと、復習しやすくなります。")


