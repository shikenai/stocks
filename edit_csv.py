import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 266)
pd.set_option('display.max_columns', 50)


def edit(df, df_date, brand_code):
    df_extracted = df.loc[:, brand_code]

    df_merged = pd.concat([df_extracted, df_date], axis=1)
    df_merged.columns = ['Close', 'High', 'Low', 'Open', 'Volume', 'Date']

    gd_df = golden_cross(df_merged)
    macd_df = set_macd(gd_df)

    print(macd_df)


def golden_cross(df):
    ma_short = df["Close"].rolling(window=5).mean()
    ma_long = df["Close"].rolling(window=20).mean()
    df = pd.concat([df, ma_short.rename('MA_short'), ma_long.rename('MA_long')], axis=1)
    df['golden_cross'] = df['MA_short'] > df['MA_long']
    df['golden_cross_shifted'] = df['golden_cross'].shift()
    df.loc[(df['golden_cross_shifted'] == False) & (df['golden_cross'] == True), 'transition_golden_cross'] = 'Gx好転'
    df.loc[(df['golden_cross_shifted'] == False) & (df['golden_cross'] == False), 'transition_golden_cross'] = '悪継続'
    df.loc[(df['golden_cross_shifted'] == True) & (df['golden_cross'] == True), 'transition_golden_cross'] = '良継続'
    df.loc[(df['golden_cross_shifted'] == True) & (df['golden_cross'] == False), 'transition_golden_cross'] = 'Dx発生'
    return df


# 指数平滑移動平均計算
def calc_ema(prices, period):
    ema = np.zeros(len(prices))
    ema[:] = np.nan  # NaN で初期化
    ema[period - 1] = prices[:period].mean()  # 最初だけ単純移動平均
    for d in range(period, len(prices)):
        ema[d] = ema[d - 1] + (prices[d] - ema[d - 1]) / (period + 1) * 2
    return ema


# MACD 計算
def calc_macd(prices, period_short, period_long, period_signal):
    ema_short = calc_ema(prices, period_short)
    ema_long = calc_ema(prices, period_long)
    macd = ema_short - ema_long  # MACD = 短期移動平均 - 長期移動平均
    signal = pd.Series(macd).rolling(period_signal).mean()  # シグナル = MACD の移動平均
    hist = macd - signal
    hist_rate = hist / prices
    return macd, signal, hist, hist_rate


def set_macd(df):
    df['macd_line'], df['macd_signal'], df['macd_hist'], df['macd_hist_rate'] = calc_macd(df.Close, 12, 26, 9)
    return df
