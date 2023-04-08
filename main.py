import pandas as pd
import os
import edit_csv
import datetime as dt
import drawer

# 初期設定諸々
t1 = dt.datetime.now()
trades_filename = 'nikkei_trades_20230408.csv'
brands_filename = 'nikkei_listed_20230314_.csv'

# pandasの表示設定
pd.set_option('display.max_rows', 267)
pd.set_option('display.max_columns', 50)

# トレードデータcsvの読み込みと初期加工
df = pd.read_csv(os.path.join(os.getcwd(), 'data', trades_filename))
new_columns = df.iloc[0].tolist()
df.columns = new_columns
df = df.drop([0, 1])
df = df.rename(columns={"Symbols": 'Date'})
df_date = df['Date']
_df = edit_csv.edit(df, df_date, '4151.jp')
base_df = pd.DataFrame(index=[], columns=list(_df.columns))
# ブランドデータcsvを読み込んでリスト化
df_brands = pd.read_csv(os.path.join(os.getcwd(), 'data', brands_filename))
df_brands['0'] = df_brands['0'].astype(str)

# トレードデータの処理
_list_brands = list(df_brands['0'])
list_brands = [b + ".jp" for b in _list_brands]
# 本当はこっち
for b in list_brands:
    temp_df = edit_csv.edit(df, df_date, b)
    base_df = pd.concat([base_df, temp_df])

# df = edit_csv.edit(df, df_date, '4151.jp')
# drawer.pair(base_df)
# print(base_df)
# print(base_df["signal_gd_macd_rsi_positive"].value_counts())
# print(base_df)
drawer.extract(base_df)
# 事後処理
elapsed_time = dt.datetime.now() - t1
minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
print(f"{minutes:.0f}分{seconds:.0f}秒")
