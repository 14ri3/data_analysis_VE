## App

## ※Slideshowでのみ使用可能
# 1. melt class
# 2. statistics class
# 3. Unmelt class



class Melt:
    def __init__(self, df):#初期化
        self.df = df #DataFrame

    def melt(self):
        import pandas as pd
        
        # カテゴリーを縦に結合
        new_df = pd.melt(
            self.df,
            id_vars=['Title', 'Pageviews', 'Original', 'Gender', 'Year-Month'],
            value_vars=['Category', 'Sub_category'],
            var_name='Category Type',
            value_name='Categories'
        )
        
        # Remove rows with NaN values in Category
        new_df = new_df.dropna(subset=['Categories'])


        # -------------------------------------------------------------------------
        # new column 'Sub': Sub_categoryがある場合、隣の行にもう一つのカテゴリーを表示
        # まず新しいカラム "Sub" を作る（デフォルトは None）
        new_df["Sub"] = None
        
        # full_df から必要なデータ（Title, Category, Sub_category）を new_full_df に結合
        new_df = new_df.merge(
            self.df[['Title', 'Category', 'Sub_category']], 
            on='Title', 
            how='left'
        )
        
        # Sub_category が NaN でない場合にのみ処理を適用
        new_df.loc[new_df["Sub_category"].notna(), "Sub"] = new_df.apply(
            lambda row: row["Sub_category"] if row["Categories"] == row["Category"] 
                        else row["Category"] if row["Categories"] == row["Sub_category"]
                        else None, 
            axis=1
        )

        # 余計なカラムを削除
        new_df=new_df.drop(columns=['Category', 'Sub_category', 'Category Type'])
        
        # Pageviews の降順にソート
        new_df = new_df.sort_values(by='Pageviews', ascending=False)


        return new_df


# ### Statistics class

# In[3]:


class Statistics:
    def __init__(self, df, origin_df, focus_column):
        self.df = df # この df は、melt　後のやつを入れてください。melt_dfが必要ない場合はfull_dfでok
        self.origin_df = origin_df # 元の（melt前のdf）
        self.focus_column = focus_column # なんのカラムにフォーカスしてまとめるのか　e.g.'Ctegories', 'Gender'

    def statistics(self):
        import pandas as pd

        # focus_columnごとの記事の個数
        article_count = self.df.groupby(self.focus_column).size().reset_index(name='Article Count')
        
        #Group by focus_column and calculate the total Pageviews
        total_PageV = self.df.groupby(self.focus_column)['Pageviews'].sum().reset_index()
        
        # focus_columnごとの PageV の最大値
        max_PageV = self.df.groupby(self.focus_column)['Pageviews'].max().reset_index(name='Max PageV')
        
        overall_mean = self.origin_df['Pageviews'].mean() # 全体の平均
        # 各focus_columnごとに平均以上の記事数を計算
        above_average_articles = self.df[self.df['Pageviews'] > overall_mean]
        above_average_count = above_average_articles.groupby(self.focus_column).size().reset_index(name='Above Average Count')
        
        # すべての統計情報を統合
        result = article_count.merge(total_PageV, on=self.focus_column, how='left')
        result = result.merge(max_PageV, on=self.focus_column, how='left')
        result = result.merge(above_average_count, on=self.focus_column, how='left')
        
        # 欠損値を 0 に置き換える（平均以上の記事がないfocus_columnなどの場合）
        result = result.fillna(0)  # NaN を 0 に置き換え
        result['Above Average Count'] = result['Above Average Count'].astype(int)  # 整数型に変換
        
        # Article count の降順にソート
        result = result.sort_values(by='Article Count', ascending=False)
        
        # Article Ratio
        total_articles = result['Article Count'].sum()# 合計の記事数
        result['Article Ratio'] = result['Article Count']/total_articles
        
        # PageV Ratio
        total_total_PageV = result['Pageviews'].sum()# 合計の記事数
        result['PageV Ratio'] = result['Pageviews']/total_total_PageV
        
        # Buzz Ratio
        result['Buzz Ratio'] = result['Above Average Count']/result['Article Count']
        
        result = result[[self.focus_column, 'Article Count', 'Pageviews', 'Max PageV', 'PageV Ratio', 'Article Ratio', 'Above Average Count', 'Buzz Ratio']]

        #---------------------------------------------------------------------
        ## Total の統計量列
        # 🔥 合計値を求める
        total_article_count = result["Article Count"].sum()
        total_pageviews = result["Pageviews"].sum()
        total_above_ave_count = result['Above Average Count'].sum()
        total_buzz_ratio = total_above_ave_count / total_article_count


                
        return result


# ## Unmelt class
# melt したDataFrameをmelt前の状態に力ずくで戻す
# （重複してるTitleのデータの片方を消す）

# In[4]:


class Unmelt:
    def __init__(self, df):
        self.df = df

    def unmelt(self):
        import pandas as pd

        unmelt_df = self.df.drop_duplicates(subset='Title', keep='first')

        # Pageviews の降順にソート
        unmelt_df = unmelt_df.sort_values(by='Pageviews', ascending=False)

        return unmelt_df


# ------------------------------------------------------------------------
# def total_pageviews(new_month_df, next_month_df):
#     new_month_df.loc[:, 'Pageviews'] = new_month_df['Title'].map(
#         lambda title: new_month_df.loc[new_month_df['Title'] == title, 'Pageviews'].sum() +
#                       next_month_df.loc[next_month_df['Title'] == title, 'Pageviews'].sum()
#     )

#     return new_month_df

import pandas as pd

# def total_pageviews(new_month_df, next_month_df):
#     # 🔥 `Pageviews` を数値型に変換（NaN の場合 0 にする）
#     new_month_df["Pageviews"] = pd.to_numeric(new_month_df["Pageviews"], errors="coerce").fillna(0)
#     next_month_df["Pageviews"] = pd.to_numeric(next_month_df["Pageviews"], errors="coerce").fillna(0)

#     # 🔥 `Title` に一致する `Pageviews` の合計を求める（NaN 回避）
#     new_month_df["Pageviews"] = new_month_df["Title"].map(
#         lambda title: new_month_df.loc[new_month_df["Title"] == title, "Pageviews"].sum() +
#                       next_month_df.loc[next_month_df["Title"] == title, "Pageviews"].sum()
#     ).fillna(0)  # 🔥 NaN を 0 に変換

#     # 降順に並べ替え
#     new_month_df.sort_values(by="Pageviews", ascending=False, inplace=True)

#     return new_month_df

def total_pageviews(new_month_df, next_month_df):
    # 数値型に変換
    new_month_df["Pageviews"] = pd.to_numeric(new_month_df["Pageviews"].replace(",", "", regex=True), errors="coerce").fillna(0)
    next_month_df["Pageviews"] = pd.to_numeric(next_month_df["Pageviews"].replace(",", "", regex=True), errors="coerce").fillna(0)
    
    # next_month_dfを辞書化 {タイトル: Pageviews} にする
    next_pageviews_dict = next_month_df.groupby("Title")["Pageviews"].sum().to_dict()
    
    # new_month_dfに対して、TitleごとにPageviewsを加算
    new_month_df["Pageviews"] = new_month_df.apply(
        lambda row: row["Pageviews"] + next_pageviews_dict.get(row["Title"], 0),
        axis=1
    )
    
    # 降順にソート
    new_month_df.sort_values(by="Pageviews", ascending=False, inplace=True)

    return new_month_df






