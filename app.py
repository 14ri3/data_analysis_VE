# 🤔 データのフィルタリングしたい

# 1. まずひと月だけでテスト
# ある月のcsvファイル読み込む
# → 特定のカラムだけにする（これ作る時、元データがどんなものなのか確認する、元データにないデータで何が必要なのか確認する）
# → meltする（class）　→ 統計量計算（class） ※実際は2月分だからこれは単なるテスト
# → melt　と　統計量　をそれぞれcsvファイルとして出力
# → ファイル名は、、「アップロードされたファイル名_data/statistics.csv」
# -------------------------------------------------------------------------
# 2. 全月合計 or　選択
# 前提：それ以前の月のをまとめたファイルを作っておく
# 新しく追加したファイルの処理
# → 前のデータと統合　※Pageviewsは2月分の合計という点に注意
# → 2つのカラム「その月のPageV」「2月分の合計PageV」　というカラムを作る

# 月を選択できるようにする
#　　meltしたやつを元に、そのデータには　どのようなYearとMonthがあるのかを表示
# >> そのためにはどのデータがどの月なのかという情報が必要
# 　　>> ファイル追加する際、それがどの年、月なのか選択　→ データフレームにその情報を追加
# -------------------------------------------------------------------------
# 3. ゆみさんのJPファイル & データcsvファイル　を組み合わせてデータの前処理簡潔にできるか検討

# 🏃‍➡️ streamlit run VE/App/app.py

import streamlit as st
from streamlit_option_menu import option_menu
import data_clean # データの前処理の前処理
import add_category # Add Categories
import add_new_month_data as addata  # 📂 ファイルアップロード用のページ
import statistics # 統計量計算

st.set_page_config(page_title="データ分析", layout="wide")

# 📌 サイドバーでページ切り替え
selected = option_menu(
    menu_title="Select what you want to do",
    options=["データの整理","データにカテゴリーを追加", "データの追加", '分析'],
    icons=["folder","tags","upload", "tools"],
    menu_icon="search",
    default_index=0,
    orientation="horizontal"
)

# 📂 **選択されたページを実行**
if selected == "データの整理":
    data_clean.show_page()
elif selected == "データにカテゴリーを追加":
    add_category.show_page()
elif selected == "データの追加":
    addata.show_page()  # `upload.py` の `show_page()` を実行
elif selected == "分析":
    statistics.show_page()



















