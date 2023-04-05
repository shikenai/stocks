import pandas as pd
import os
import edit_csv
import datetime as dt

t1 = dt.datetime.now()
pd.set_option('display.max_rows', 266)
pd.set_option('display.max_columns', 50)
df = pd.read_csv(os.path.join(os.getcwd(), 'data', 'nikkei_trades_20220301.csv'))
new_columns = df.iloc[0].tolist()
df.columns = new_columns
df = df.drop([0, 1])
df = df.rename(columns={"Symbols": 'Date'})
df_date = df['Date']

df_brands = pd.read_csv(os.path.join(os.getcwd(), 'data', 'nikkei_listed_20230314_.csv'))
df_brands['0'] = df_brands['0'].astype(str)

_list_brands = list(df_brands['0'])
list_brands = [b + ".jp" for b in _list_brands]
# 本当はこっち
# for b in list_brands:
#     edit_csv.edit(df, df_date, b)

edit_csv.edit(df, df_date, '4151.jp')

elapsed_time = dt.datetime.now() - t1
minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
print(f"{minutes:.0f}分{seconds:.0f}秒")
