import streamlit as st
import pandas as pd
import class_melt_statistics as ms

def show_page(): 
    st.title("データにカテゴリーなどを追加")
    st.write("")
    st.write("") 

    # 🩵 cleaned_data
    st.write("📂 cleaned_data.csv をアップロードしてください。")
    new_month_file = st.file_uploader(label="※項目：Title, Pageviews, Original, Category, Sub_category, Gender", type=["csv"], key="file_new")
    st.write("") 
    st.write("") 

    # 🩵 category が書かれてあるファイル
    category_file = st.file_uploader(label="📂 その月のデータのカテゴリーが書かれてあるCSVファイルをアップロードしてください。", type=["csv"], key="file_next")
    st.write("")
    st.write("")
    st.write("")

# -------------------------------------------------------------------------
    if new_month_file is not None and category_file is not None:
        st.markdown('<p style="color:red;">⚠️ ファイルをアップロードし直したい場合は、ページをリフレッシュしてください</p>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # CSVをDataFrameに読み込む
        new_month_df = pd.read_csv(new_month_file)
        category_df = pd.read_csv(category_file)
        
        # =================================================================

        ## 🏷️ Category などを追加する
        # 1️⃣　必要な列だけcategory_dfから持ってくる　（just in case）
        category_columns = ["Title", "Original", "Category", "Sub_category", "Gender"]
        category_df_subset = category_df[category_columns]
        
        # 2️⃣　Titleでマージ（left join）
        new_month_df = new_month_df.merge(
            category_df_subset,
            on="Title",
            how="left",
            suffixes=("", "_from_cat")  # 競合カラム対策
        )

        # 3️⃣ NaN部分だけをcategory_dfから補完（combine_first()）
        for col in ["Original", "Category", "Sub_category", "Gender"]:
            new_month_df[col] = new_month_df[col].combine_first(new_month_df[col + "_from_cat"])
        
        # 4️⃣ 補助カラムを削除
        new_month_df.drop(columns=[col + "_from_cat" for col in ["Original", "Category", "Sub_category", "Gender"]], inplace=True)


        # -----------------------------------------------------------------
        # Title だけ取り出して集合型にする
        new_titles = set(new_month_df["Title"])
        category_titles = set(category_df_subset["Title"])
        
        # 一致しないものを探す（差集合）
        missing_titles = new_titles - category_titles
        
        if missing_titles:
            st.warning("⚠️ 以下のタイトルの記事は、ダウンロード後に手動で編集・削除等してください:")
            for title in missing_titles:
                st.write(f"- {title}")
        else:
            st.success("✅ 全てのタイトルにおいてカテゴリーなどが追加されました！")

        st.markdown("<hr>", unsafe_allow_html=True)
        
        # 表示、ダウンロード
        st.write(new_month_df)
        # 📥　ダウンロード
        csv_add_cat = new_month_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 カテゴリーなどが追加されたCSVファイルをダウンロードしてください",
            data=csv_add_cat,
            file_name='complete_data.csv',
            mime="text/csv",
        )

        st.write('ダウンロードされるCSVファイルの名前：complete_data')


# -------------------------------------------------------------------------
















