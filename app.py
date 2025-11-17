import streamlit as st

# -----------------------------
# ページ全体の設定
# -----------------------------
st.set_page_config(
    page_title="Git 用語ミニ辞典",
    layout="wide"
)

st.title("Git 用語ミニ辞典")

st.write("左のリストから用語を選ぶと、右側に説明が表示されます。")


# -----------------------------
# 用語データ定義
# -----------------------------
TERMS = {
    "リポジトリ（repository）": {
        "category": "Git / GitHub",
        "meaning": "フォルダ全体の履歴を保存する場所（プロジェクトのタイムマシン）。",
        "description": """
### OneDrive と Git の違いで理解するリポジトリ

#### 1. 管理する単位が違う
**OneDrive**
- ファイルの過去版を最大 500 個まで保持
- 管理しているのは「ファイル単体」

**Git（リポジトリ）**
- フォルダ全体の「その瞬間の状態」を保存
- 履歴は無制限
- 管理しているのは「フォルダ丸ごと」

#### 2. 壊したときに戻せる範囲が違う
**OneDrive**
- 消したファイルだけ戻せる
- フォルダ全体の構成は戻らない

**Git**
- フォルダ丸ごと過去の状態に戻せる
- うっかりフォルダを削除しても復元できる

#### 3. 履歴の作られ方が違う
**OneDrive**
- 修正前の「ファイルのコピー」をそのまま保存

**Git**
- 変わった部分だけ新しく保存
- 変わっていない部分は過去のデータを再利用
- それでも「フォルダ全体の完全なスナップショット」が残る

#### 重要ポイント
- リポジトリ = フォルダ全体の履歴の倉庫
- OneDrive のような“ファイル単体”管理ではない
- 過去状態にフォルダごと戻せる
- 履歴数は無制限
"""
    },
    "リモートリポジトリ（remote repository）": {
        "category": "Git / GitHub",
        "meaning": "インターネット上にある、みんなで共有するリポジトリ。",
        "description": """
- GitHub や Azure DevOps 上にあるリポジトリ
- チーム全員が push / pull する“共有の本棚”
- 自分の PC には履歴のコピー（ローカルリポジトリ）がある
"""
    },
    "ローカルリポジトリ（local repository）": {
        "category": "Git / GitHub",
        "meaning": "自分の PC 上にあるリポジトリ。",
        "description": """
- 自分専用のタイムマシン
- コミットまではローカルだけで完結
- 仕事が一区切りついたら、push でリモートに送る
"""
    },
    "ベアリポジトリ（bare repository）": {
        "category": "Git / GitHub",
        "meaning": "作業フォルダを持たず、履歴データだけを持つリポジトリ。",
        "description": """
- `.git` の中身だけがある特殊なリポジトリ
- ファイルを直接編集することはできない
- 共有専用（サーバー側）として使われる
- GitHub の中身はベアリポジトリと同じ構造
"""
    },
    "ノンベアリポジトリ（non bare repository）": {
        "category": "Git / GitHub",
        "meaning": "履歴と作業フォルダの両方を持つ、ふつうのリポジトリ。",
        "description": """
- `.git`（履歴）＋ ワークツリー（作業フォルダ）がセット
- 開発者が普段触っているのはこちら
- PC 上のプロジェクトフォルダ = ノンベアリポジトリ
"""
    },
    "ワークツリー（work tree）": {
        "category": "Git / GitHub",
        "meaning": "実際にファイルを開いたり編集したりする作業用フォルダ。",
        "description": """
- VS Code で開いているフォルダの中身そのもの
- `.git` に保存されている履歴を、ここに展開して作業する
- ブランチを切り替えると、ワークツリーの中身も切り替わる
"""
    },
    "インデックス（index）／ステージ（stage）": {
        "category": "Git / GitHub",
        "meaning": "「次のコミットに含める変更」を一時的に置いておく場所。",
        "description": """
- ステージングエリアとも呼ばれる
- `git add` でインデックスに変更を入れる
- インデックスにある変更だけが、次のコミットに含まれる
- イメージ：レジに持って行く前の“買い物カゴ”
"""
    },
    "ハンク（hunk）": {
        "category": "Git / GitHub",
        "meaning": "1つのファイルの変更の中の“ひとかたまり”。",
        "description": """
- ファイル全体ではなく、変更行のグループ
- `git add -p` などで「この部分だけステージ」するときの単位
- 不要な変更をコミットに混ぜないために使う
"""
    },
    "コミット（commit）": {
        "category": "Git / GitHub",
        "meaning": "フォルダ全体の状態を保存する“スナップショット”。",
        "description": """
- その時点のプロジェクトの状態を丸ごと記録
- メッセージを付けて「何をしたコミットか」を残す
- OneDrive の保存より強力（フォルダ全体＆無制限）
"""
    },
    "リセット（reset）": {
        "category": "Git / GitHub",
        "meaning": "現在地（HEAD）を過去のコミットに戻す操作。",
        "description": """
- タイムマシンで「この時点まで巻き戻す」イメージ
- `--soft` / `--mixed` / `--hard` で戻し方の強さが変わる
- 強い reset は取り戻せないこともあるので要注意
"""
    },
    "ヘッド（HEAD）": {
        "category": "Git / GitHub",
        "meaning": "「いま見ているコミット」を指しているポインタ。",
        "description": """
- 本でいう「いま読んでいるページに挟んだしおり」
- ブランチを切り替えると、HEAD の指す先も変わる
"""
    },
    "チェックアウト（checkout）": {
        "category": "Git / GitHub",
        "meaning": "HEAD を別のブランチやコミットに切り替える操作。",
        "description": """
- 「どの時点のフォルダ状態をワークツリーに展開するか」を変える
- ブランチの切り替えも、古いコミットの中身を見るのも checkout
"""
    },
    "プッシュ（push）": {
        "category": "Git / GitHub",
        "meaning": "ローカルのコミットをリモートリポジトリに送ること。",
        "description": """
- 自分の手元の履歴を、共有リポジトリに反映する
- チームへの“成果物の提出”に相当
"""
    },
    "プル（pull）": {
        "category": "Git / GitHub",
        "meaning": "リモートの変更を取り込み、自分のブランチに統合すること。",
        "description": """
- 実際には「fetch（取得）＋ merge（統合）」をまとめて行う操作
- チームメンバーの最新変更を自分の作業に反映させる
"""
    },
    "フェッチ（fetch）": {
        "category": "Git / GitHub",
        "meaning": "リモートの最新履歴を“確認用”として取ってくる操作。",
        "description": """
- ローカルのブランチはまだ書き換えない
- まず fetch して差分を見てから、必要に応じて merge / rebase する
- 安全に様子を見るための操作
"""
    },
    "マージ（merge）": {
        "category": "Git / GitHub",
        "meaning": "別々のブランチでの作業を1つにまとめること。",
        "description": """
- それぞれの変更を統合して、新しいコミットを作る
- 同じ場所を編集していない限り、自動でくっつく
- 同じ行を違う内容で変えているとコンフリクトになる
"""
    },
    "リベース（rebase）": {
        "category": "Git / GitHub",
        "meaning": "自分のブランチの土台を、より新しいコミットに付け替えること。",
        "description": """
- 自分のコミットを“最新の main の上に積み直す”操作
- 履歴が一直線になり、見通しが良くなる
- 履歴を書き換えるため、共有後のブランチでは注意が必要
"""
    },
    "コンフリクト（conflict）": {
        "category": "Git / GitHub",
        "meaning": "同じ場所を複数人が違う内容で編集し、どちらを採用するか決められない状態。",
        "description": """
- Git が自動でマージできず、人間の判断が必要な状態
- 該当ファイルに >>>>>> / <<<<<< のような記号が入る
- どの内容を残すかを手作業で直してから、再度コミットする
"""
    },
    "ブランチ（branch）": {
        "category": "Git / GitHub",
        "meaning": "プロジェクトフォルダの“作業用コピー”を作る仕組み。",
        "description": """
- main（本線）とは別の作業レーンを作れる
- 各ブランチで自由にコミットし、あとで merge して統合
- OneDrive で同じファイルを上書きし合うのとは違い、安全に並行作業できる
"""
    },
    "フォーク（fork）": {
        "category": "Git / GitHub",
        "meaning": "他人のリポジトリを、自分のアカウント配下に丸ごとコピーすること。",
        "description": """
- GitHub 上で行う操作
- オリジナルとは別の“自分用プロジェクト”として開発を進められる
- OSS へのコントリビューションでよく使う
"""
    },
    "クローン（clone）": {
        "category": "Git / GitHub",
        "meaning": "リモートリポジトリを丸ごとローカルにコピーすること。",
        "description": """
- `git clone URL` で実行
- 履歴ごとコピーされるので、過去の状態もすべて手元で見られる
- 作業を始める最初の一手
"""
    },
    "プルリクエスト（pull request）": {
        "category": "Git / GitHub",
        "meaning": "「自分のブランチの変更を main に取り込んでください」と依頼する仕組み。",
        "description": """
- GitHub / Azure DevOps 上のレビュー用機能
- コードレビュー、コメント、テスト結果の確認などをここで行う
- 承認されたら main などにマージされる
"""
    },
    ".gitignore": {
        "category": "Git / GitHub",
        "meaning": "Git に「このファイルは履歴に入れないで」と指示する設定ファイル。",
        "description": """
- ビルド成果物、ログ、キャッシュ、秘密情報などを除外する
- 誤って機密情報や巨大ファイルをコミットしないための安全装置
"""
    },
    ".gitignore（グローバル）": {
        "category": "Git / GitHub",
        "meaning": "PC 全体のすべてのリポジトリに共通で適用される .gitignore。",
        "description": """
- OS 固有ファイル（Thumbs.db, .DS_Store など）をまとめて無視したいときに使う
- ユーザーごとの Git 設定でパスを登録する
- プロジェクトごとの .gitignore と併用できる
"""
    },
}

# ラベルの順番を固定
term_labels = list(TERMS.keys())

# -----------------------------
# レイアウト
# -----------------------------
left_col, right_col = st.columns([1, 2])

with left_col:
    selected_label = st.radio(
        "用語を選択",
        term_labels,
        index=0
    )

with right_col:
    term = TERMS[selected_label]
    st.subheader(selected_label)
    st.markdown(f"**カテゴリ：** {term['category']}")
    st.markdown(f"**意味：** {term['meaning']}")
    st.markdown("---")
    st.markdown(term["description"])
