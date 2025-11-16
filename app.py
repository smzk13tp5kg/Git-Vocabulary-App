import streamlit as st

# ---- 用語データ ----
TERMS = [
    {"category": "Git / GitHub", "term": "リポジトリ", "english": "repository",
     "meaning": "履歴管理を行う場所。"},
    {"category": "Git / GitHub", "term": "リモートリポジトリ", "english": "remote repository",
     "meaning": "サーバーにあるリポジトリ。基本はベアリポジトリで運用される。"},
    {"category": "Git / GitHub", "term": "ローカルリポジトリ", "english": "local repository",
     "meaning": "自分のPCにあるリポジトリ。基本はノンベアリポジトリで運用される。"},
    {"category": "Git / GitHub", "term": "ベアリポジトリ", "english": "bare repository",
     "meaning": "ワークツリーを持たず、チェックアウト、マージができないリポジトリ。"},
    {"category": "Git / GitHub", "term": "ノンベアリポジトリ", "english": "non bare repository",
     "meaning": "ワークツリーを持ち、チェックアウト、マージができるリポジトリ。"},
    {"category": "Git / GitHub", "term": "ワークツリー", "english": "work tree",
     "meaning": "履歴管理を行いたいファイルがある場所。"},
    {"category": "Git / GitHub", "term": "インデックス", "english": "index",
     "meaning": "コミットしたいファイル又はファイルの一部を登録するところ。"},
    {"category": "Git / GitHub", "term": "ステージ", "english": "stage",
     "meaning": "ワークツリーからコミットしたいファイル又はファイルの一部をIndexに登録すること。"},
    {"category": "Git / GitHub", "term": "ハンク", "english": "hunk",
     "meaning": "変更した一範囲。"},
    {"category": "Git / GitHub", "term": "コミット", "english": "commit",
     "meaning": "インデックスに登録してある変更対象をローカルリポジトリに反映すること。"},
    {"category": "Git / GitHub", "term": "リセット", "english": "reset",
     "meaning": "コミット前の変更をローカルリポジトリの状態へ戻すこと。また、特定のコミットまで状態を戻すこと。ただし、ローカルリポジトリに限られる。"},
    {"category": "Git / GitHub", "term": "ヘッド", "english": "head",
     "meaning": "作業対象となっているブランチ、コミット。"},
    {"category": "Git / GitHub", "term": "チェックアウト", "english": "checkout",
     "meaning": "ヘッドを切り替えること。過去のコミットを対象にチェックアウトした場合、それをもとにコミットすることはできない。"},
    {"category": "Git / GitHub", "term": "プッシュ", "english": "push",
     "meaning": "ローカルリポジトリの変更をリモートリポジトリに反映させること。"},
    {"category": "Git / GitHub", "term": "プル", "english": "pull",
     "meaning": "リモートリポジトリの変更をローカルリポジトリに反映させること。フェッチ＋マージ。"},
    {"category": "Git / GitHub", "term": "フェッチ", "english": "fetch",
     "meaning": "リモートリポジトリの変更をローカルに取得すること。（マージは行わない）。"},
    {"category": "Git / GitHub", "term": "マージ", "english": "merge",
     "meaning": "異なるブランチの変更を反映させること。お互いの変更履歴が残る。"},
    {"category": "Git / GitHub", "term": "リベース", "english": "rebase",
     "meaning": "異なるブランチの変更を反映させること。変更履歴が片方に集約される。"},
    {"category": "Git / GitHub", "term": "コンフリクト", "english": "conflict",
     "meaning": "マージ対象の２ファイルで同じ箇所が変更されており、自動でマージができないこと。"},
    {"category": "Git / GitHub", "term": "ブランチ", "english": "branch",
     "meaning": "履歴管理を枝分かれさせたもの。ブランチを使うことで複数の履歴を並列に管理できる。"},
    {"category": "Git / GitHub", "term": "フォーク", "english": "fork",
     "meaning": "リモートリポジトリをコピーしてリモートリポジトリを作成すること。"},
    {"category": "Git / GitHub", "term": "クローン", "english": "clone",
     "meaning": "リモートリポジトリをコピーしてローカルリポジトリを作成すること。"},
    {"category": "Git / GitHub", "term": "プルリクエスト", "english": "pull request",
     "meaning": "フォークしたリポジトリでの変更を、フォーク元のリポジトリへ反映するよう依頼すること。"},
    {"category": "Git / GitHub", "term": ".gitignore", "english": ".gitignore",
     "meaning": "履歴管理の対象外とするファイルを登録するところ。対象範囲は各リポジトリ。"},
    {"category": "Git / GitHub", "term": ".gitignore（グローバル）", "english": ".gitignore (global)",
     "meaning": "履歴管理の対象外とするファイルを登録するところ。対象範囲は全リポジトリ。"},
]

# ---- アプリ本体 ----
st.set_page_config(page_title="Git用語ナビ", layout="wide")

st.title("Git 用語ナビ")
st.write("「これって何のこと？どこで使うの？」というGit用語を、一覧・検索できるミニ辞典です。")

keyword = st.text_input("キーワード検索（用語・英語・説明から部分一致）")

filtered = TERMS
if keyword:
    kw = keyword.lower()
    filtered = [
        t for t in TERMS
        if kw in t["term"].lower()
        or kw in t["english"].lower()
        or kw in t["meaning"].lower()
    ]

st.write(f"ヒット件数：{len(filtered)}")

if not filtered:
    st.info("条件に合う用語がありません。キーワードを変えてみてください。")
else:
    col_list, col_detail = st.columns([1, 2])

    with col_list:
        labels = [f'{t["term"]}（{t["english"]}）' for t in filtered]
        selected_label = st.radio("用語を選択", labels)
        selected = filtered[labels.index(selected_label)]

    with col_detail:
        st.subheader(f'{selected["term"]}（{selected["english"]}）')
        st.markdown(f'**カテゴリ**：{selected["category"]}')
        st.markdown(f'**意味**：{selected["meaning"]}')
