import streamlit as st
import pandas as pd
import class_melt_statistics as ms

def show_page(): 
    st.title("新しい月のデータの整理")
    st.write('')

    # ------------------------------------------------------------------------
    # 🩵 that month　⚠️ファイル削除するだけじゃこれは消えない
    new_month_file = st.file_uploader(label="📂 追加したい月のCSVファイルをアップロードしてください。", type=["csv"], key="file_new")
    
    st.write("") 
    st.write("") 

    #　🩵 previous month　→ その月の記事を抽出する用
    st.write('📂 その前までの月のCSVファイルをアップロードしてください。')
    previous_month_file = st.file_uploader("（過去に「データの追加」ページでダウンロードしたCSVファイル。追加したい月の前の全てのデータを含めてください）", type=["csv"], key="file_previous")

    
    # ------------------------------------------------------------------------
    if new_month_file is not None and previous_month_file is not None:
        # DataFrame化
        st.markdown('<p style="color:red;">⚠️ ファイルをアップロードし直したい場合は、ページをリフレッシュしてください</p>', unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        new_month_df = pd.read_csv(new_month_file)
        previous_month_df = pd.read_csv(previous_month_file)
        # ---------------------------------------------------------------------
        # Japan Market、Gallery Content だけ抽出
        try:
            new_month_df = new_month_df[(new_month_df['Market'] == 'Japan') & (new_month_df['Content type'] == 'Gallery')]
        except:
            st.write('🚨 アップロードされたデータの項目に"Market", "Content type"が無いため処理できません。')
            st.write('①日本の記事のみ②Slideshowのみ　になっているか確認し、なっていない場合は手動で直してください。')
            
        else:
            # Title, Pageviews　カラムだけ残す
            new_month_df = new_month_df[["Title", "Pageviews"]]

            # 必要なカラム追加
            new_month_df[["Original", "Category", "Sub_category", "Gender"]] = None

            # その月で publish された記事だけ抽出
            previous_titles = previous_month_df['Title']
            new_month_df = new_month_df[~new_month_df['Title'].isin(previous_titles)]

            st.write(new_month_df)#del
            
            # 📥　ダウンロード
            csv_clean = new_month_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 整理されたCSVファイルをダウンロードしてください",
                data=csv_clean,
                file_name='cleaned_data.csv',
                mime="text/csv",
            )

            st.markdown("<hr>", unsafe_allow_html=True)
            #st.write('ダウンロードしたファイルを編集（Categoryの追加など）して、')
            #st.write('編集した後のファイルを「データの追加」ページで使用してください ✏️')

            st.write('ダウンロードされるCSVファイルの名前：cleaned_data')

            




















        