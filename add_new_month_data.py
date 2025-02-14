import streamlit as st
import pandas as pd
import class_melt_statistics as ms

def show_page(): 
    st.title("新しい月のデータを追加")
    st.write("")
    st.write("") 

    # 🩵 that month　⚠️ファイル削除するだけじゃこれは消えない
    st.write("📂 complete_data.csvをアップロードしてください。")
    new_month_file = st.file_uploader(label="※項目：Title, Pageviews, Original, Category, Sub_category, Gender", type=["csv"], key="file_new")
    st.write("") 
    st.write("") 

    # 🩵 next month　→ 2ヶ月分のPageviews　合計する用
    next_month_file = st.file_uploader(label="📂 その次の月のCSVファイルをアップロードしてください。", type=["csv"], key="file_next")
    st.write("")
    st.write("")
    st.write("")
    
    #　🩵 previous month　→ その月の記事を抽出する用
    st.write('📂 その前までの月のCSVファイルをアップロードしてください。')
    previous_month_file = st.file_uploader("（過去にこのページでダウンロードしたCSVファイル。追加したい月の前の全てのデータを含めてください）", type=["csv"], key="file_previous")

# -------------------------------------------------------------------------
    if new_month_file is not None and next_month_file is not None and previous_month_file is not None:
        st.markdown('<p style="color:red;">⚠️ ファイルをアップロードし直したい場合は、ページをリフレッシュしてください</p>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # CSVをDataFrameに読み込む
        new_month_df = pd.read_csv(new_month_file)
        next_month_df = pd.read_csv(next_month_file)
        previous_month_df = pd.read_csv(previous_month_file)
        st.session_state["next_month_df"] = next_month_df # Global
        st.session_state["previous_month_df"] = previous_month_df # Global
        # -------------------------------------------------------------------　
        # 📅 ユーザーから年月を選択してもらう
        col1, col2 = st.columns(2)
        with col1:
            year = st.selectbox("追加ファイルの年（YYYY）を選択してください", list(range(2024, 2030)))
        with col2:
            month = st.selectbox("月（MM）を選択してください", list(range(1, 13))) 
    
        # ✨ 「年月」カラムを追加
        if st.button("年月をデータに追加 & 表示"):
            
            new_month_df["Year"] = year
            new_month_df["Month"] = month
            #Global　変数
            st.session_state["Year"] = year
            st.session_state["Month"] = month
            
            # Year-Month
            new_month_df["Year-Month"] = pd.to_datetime(new_month_df["Year"].astype(str) + "-" + new_month_df["Month"].astype(str))

            st.markdown("<hr>", unsafe_allow_html=True)
            st.write(f"✅ 年月を追加しました：{year}年{month}月")
    
            # データフレームの値を保持
            st.session_state["new_month_df"] = new_month_df# del?

# ------------------------------------------------------------------------
            ## 2ヶ月分合計
            if 'new_month_df' in st.session_state:
                # Global変数をローカル変数に代入
                new_month_df = st.session_state["new_month_df"]# del?
                next_month_df = st.session_state["next_month_df"]# del?
    
                # 🛠 すでに計算されたデータがあるかチェック
                if "2m_total_df" not in st.session_state:
                    st.session_state["2m_total_df"] = ms.total_pageviews(new_month_df, next_month_df)  # 計算して保存　🤲　Page2で使う

                else:
                    st.session_state["2m_total_df"]["Year-Month"] = new_month_df["Year-Month"]
                    # Year, Month カラムを削除
                    st.session_state["2m_total_df"]['Year'] = new_month_df['Year']
                    st.session_state["2m_total_df"]['Month'] = new_month_df['Month']

                # ✅ 計算後のデータを表示（リフレッシュしても再計算されない）
                st.write(st.session_state["2m_total_df"])# del

# -------------------------------------------------------------------------
            ## 🔥 データを縦に結合
            # ✅ 項目が一致するかチェック
            new_month_df = st.session_state["2m_total_df"]
            if set(previous_month_df.columns) != set(new_month_df.columns):
                st.write("⚠️その前までの月のCSVファイルのデータの項目が一致しません！")
                st.write(previous_month_df)# del
                st.write(f"期待される項目: {set(new_month_df.columns)}")
                st.write(f"アップロードされたデータの項目: {set(previous_month_df.columns)}")
            # 🔥 項目が一致していれば結合
            else:
                All_df = pd.concat([previous_month_df, new_month_df], ignore_index=True)

                # 降順に並べ替え
                All_df = All_df.sort_values(by="Pageviews", ascending=False)

                # datetime型に変換
                All_df["Year-Month"] = pd.to_datetime(All_df["Year-Month"], errors="coerce")
                
                # 出力
                st.markdown("<hr>", unsafe_allow_html=True)
                st.write('🔗 結合したデータ：',All_df)

                # 📥　ダウンロード
                csv_all = All_df.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 結合したデータのCSVファイルをダウンロード",
                    data=csv_all,
                    file_name=str(year) + '_' + str(month) + '_all_data.csv',
                    mime="text/csv",
                )
                st.write('ここでダウンロードしたファイルを「分析」ページでアップロードしてください 🚀')
                st.write('cleaned_data.csv, complete_data.csv は削除して構いません')
# -------------------------------------------------------------------------
    # 📄 分析ページに移動
    st.write('')    
    if "2m_total_df" in st.session_state:
        #表示用にローカル変数化
        year=st.session_state["Year"]
        month=st.session_state["Month"]

        st.markdown("<hr>", unsafe_allow_html=True)
        st.write(f'新しい月（{year}年{month}月）のデータが追加されました！')
        #st.write('分析ページに移動してください')
        

# -------------------------------------------------------------------------


    else:
        st.write('まだ操作は完了していません')


# -------------------------------------------------------------------------