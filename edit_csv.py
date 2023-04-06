import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 266)
pd.set_option('display.max_columns', 50)


def edit(df, df_date, brand_code):
    df_extracted = df.loc[:, brand_code]

    df_merged = pd.concat([df_extracted, df_date], axis=1)
    df_merged.columns = ['Close', 'High', 'Low', 'Open', 'Volume', 'Date']

    # gd_df = golden_cross(df_merged)
    macd_df = add_macd(df_merged)

    print(macd_df)


def golden_cross(df):
    # ゴールデンクロス関係の処理
    ma_short = df["Close"].rolling(window=5).mean()
    ma_long = df["Close"].rolling(window=20).mean()
    df = pd.concat([df, ma_short.rename('MA_short'), ma_long.rename('MA_long')], axis=1)
    df['golden_cross'] = df['MA_short'] > df['MA_long']
    df['golden_cross_shifted'] = df['golden_cross'].shift()
    df.loc[(df['golden_cross_shifted'] == False) & (df['golden_cross'] == True), 'transition_golden_cross'] = 'Gx好転'
    df.loc[(df['golden_cross_shifted'] == False) & (df['golden_cross'] == False), 'transition_golden_cross'] = '悪継続'
    df.loc[(df['golden_cross_shifted'] == True) & (df['golden_cross'] == True), 'transition_golden_cross'] = '良継続'
    df.loc[(df['golden_cross_shifted'] == True) & (df['golden_cross'] == False), 'transition_golden_cross'] = 'Dx発生'
    df = df.drop('golden_cross_shifted', axis=1)
    return df

def add_status_boolean_change(df, col_name):
    df[f'{col_name}_shifted'] = df[col_name].shift()
    df.loc[(df[f'golden_cross_shifted'] == False) & (df['golden_cross'] == True), 'transition_golden_cross'] = 'Gx好転'
    df.loc[(df[f'golden_cross_shifted'] == False) & (df['golden_cross'] == False), 'transition_golden_cross'] = '悪継続'
    df.loc[(df[f'golden_cross_shifted'] == True) & (df['golden_cross'] == True), 'transition_golden_cross'] = '良継続'
    df.loc[(df[f'golden_cross_shifted'] == True) & (df['golden_cross'] == False), 'transition_golden_cross'] = 'Dx発生'
    df = df.drop(f'golden_cross_shifted', axis=1)



# MACD 計算
# def add_macd(df):
#     ema12 = df['Close'].ewm(span=12, adjust=False).mean()
#     ema26 = df['Close'].ewm(span=26, adjust=False).mean()
#     macd = ema12 - ema26
#     signal = macd.ewm(span=9, adjust=False).mean()
#     hist = macd - signal
#     macd_df = pd.DataFrame({'macd': macd, 'signal': signal, 'hist': hist})
#     return pd.concat([df, macd_df], axis=1)
