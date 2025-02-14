import streamlit as st
import pandas as pd
import class_melt_statistics as ms

def show_page(): 
    st.title("分析")
# ------------------------------------------------------------------------
    # 🩵 今までのデータをアップロード
    st.write('')
    st.write('')
    upload_file = st.file_uploader("📂 全てのデータのCSVファイルをアップロードしてください。", type=["csv"], key="file_new")
    
    # 全てのデータ
    if upload_file is not None: # 一番最初のみ実行
        All_df = pd.read_csv(upload_file)
        
        # datetime型に変換
        All_df["Year-Month"] = pd.to_datetime(All_df["Year-Month"], errors="coerce")
# ------------------------------------------------------------------------
        # 出力 del
        if 'All_df' not in st.session_state:
            st.write('アップロードしたデータ：',All_df)
            st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================================
        ## フィルタリング
        # 📅 ユーザーに年・月を選択してもらう
        # データフレームに存在する 年 と 月 を抽出してリスト化
        years = sorted(All_df["Year-Month"].dt.year.unique())
        months = sorted(All_df["Year-Month"].dt.month.unique())
        
        # 📅 開始年月・終了年月を選択してもらう
        st.write('📆 分析したいデータの期間を選択してください')
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.selectbox("開始年", years, index=0)
            # その年に存在する月だけをフィルタリング
            start_months = sorted(All_df[All_df["Year-Month"].dt.year == start_year]["Year-Month"].dt.month.unique())
            start_month = st.selectbox("開始月", start_months)
        
        with col2:
            end_year = st.selectbox("終了年", years, index=len(years) - 1)
            end_months = sorted(All_df[All_df["Year-Month"].dt.year == end_year]["Year-Month"].dt.month.unique())
            end_month = st.selectbox("終了月", end_months)
        
        # 🔥 入力からdatetime型に変換（月初に統一）
        start_date = pd.to_datetime(f"{start_year}-{start_month:02d}-01")
        end_date = pd.to_datetime(f"{end_year}-{end_month:02d}-01")
        
        # 🔥 フィルタリング
        filtered_df = All_df[
            (All_df["Year-Month"] >= start_date) & (All_df["Year-Month"] <= end_date)
        ]
        # 📅 期間表示用に年月を文字列に変換
        start_str = start_date.strftime("%Y年%m月")
        end_str = end_date.strftime("%Y年%m月")

        st.write('')
        st.write(f"📅 {start_str}〜{end_str} のデータ：")
        st.dataframe(filtered_df)
        st.write('このデータを下の分析で使います 🔽')
        st.markdown("<hr>", unsafe_allow_html=True)

# =========================================================================
        ### 分析の対象ごとに分ける
        focus_list = ['選択してください', 'カテゴリー', '性別']
        focus_on = st.selectbox('📍 分析したい対象を選択してください', focus_list)
        
        # ------------------------------------------------------------------------
        ## カテゴリーごとに分析
        if focus_on == 'カテゴリー':
            # クラスMelt を使用してMelt
            obj_melt = ms.Melt(filtered_df)
            melt_filtered_df = obj_melt.melt()
            #st.write("📊 Melt 後のデータ:", melt_All_df)# del

            # クラス Statistics　で
            obj = ms.Statistics(melt_filtered_df, filtered_df, 'Categories')
            statistics = obj.statistics()
            
        # ------------------------------------------------------------------------
            ## Total の統計量列
            # 🔥 合計値を求める
            total_article_count = statistics["Article Count"].sum()
            total_pageviews = statistics["Pageviews"].sum()
            total_above_ave_count = statistics['Above Average Count'].sum()
            total_buzz_ratio = total_above_ave_count / total_article_count
            
            # 📝 合計行を作成
            total_row = pd.DataFrame({
                "Categories": ["Total"],
                "Article Count": [total_article_count],
                "Pageviews": [total_pageviews],
                "Max PageV": [None],  # Noneでもnp.nanでもOK
                'PageV Ratio': [None],
                'Article Ratio': [None],
                'Above Average Count': [total_above_ave_count],
                'Buzz Ratio': [total_buzz_ratio]
            })

            # 🔄 データフレームに行を追加
            statistics = pd.concat([statistics, total_row], ignore_index=True)
            st.write(statistics)

        # ------------------------------------------------------------------------
            # 📥　ダウンロード
            csv_sta = statistics.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 結合したデータのCSVファイルをダウンロード",
                data=csv_sta,
                file_name=f'{start_year}{start_month}_{end_year}{end_month}_analysis_Catego.csv',
                mime="text/csv",
            )

        # ------------------------------------------------------------------------
        ## 性別ごとに分析
        if focus_on == '性別':
            # クラス Statistics　で
            obj = ms.Statistics(filtered_df, filtered_df, 'Gender')
            statistics = obj.statistics()
            # --------------------------------------------------------------------
            ## Total の統計量列
            # 🔥 合計値を求める
            total_article_count = statistics["Article Count"].sum()
            total_pageviews = statistics["Pageviews"].sum()
            total_above_ave_count = statistics['Above Average Count'].sum()
            total_buzz_ratio = total_above_ave_count / total_article_count
            
            # 📝 合計行を作成
            total_row = pd.DataFrame({
                "Gender": ["Total"],
                "Article Count": [total_article_count],
                "Pageviews": [total_pageviews],
                "Max PageV": [None],  # Noneでもnp.nanでもOK
                'PageV Ratio': [None],
                'Article Ratio': [None],
                'Above Average Count': [total_above_ave_count],
                'Buzz Ratio': [total_buzz_ratio]
            })

            # 🔄 データフレームに行を追加
            statistics = pd.concat([statistics, total_row], ignore_index=True)
            st.write(statistics)


            # 📥　ダウンロード
            csv_sta = statistics.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 分析結果のCSVファイルをダウンロード",
                data=csv_sta,
                file_name=f'{start_year}{start_month}_{end_year}{end_month}_analysis_Gender.csv',
                mime="text/csv",
            )








            