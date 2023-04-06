import numpy as np
import pandas as pd

pd.set_option('display.max_rows', 266)
pd.set_option('display.max_columns', 50)


def edit(_df, df_date, brand_code):
    df_extracted = _df.loc[:, brand_code]

    df = pd.concat([df_extracted, df_date], axis=1)
    df.columns = ['Close', 'High', 'Low', 'Open', 'Volume', 'Date']
    pd.set_option('display.max_rows', 267)
    pd.set_option('display.max_columns', 50)
    df = df.astype({'Close': float, 'High': float, 'Open': float, 'Low': float, 'Volume': float})
    df = add_macd(df)
    df = add_rsi(df)
    print(df)


def golden_cross(df):
    # ゴールデンクロス関係の処理
    ma_short = df["Close"].rolling(window=5).mean()
    ma_long = df["Close"].rolling(window=20).mean()
    df = pd.concat([df, ma_short.rename('MA_short'), ma_long.rename('MA_long')], axis=1)
    df['golden_cross'] = df['MA_short'] > df['MA_long']
    df = add_status_boolean_change(df, 'golden_cross')
    return df


# MACD 計算
def add_macd(df):
    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    # macd_df = pd.DataFrame({'macd': macd, 'signal': signal, 'hist': hist})
    macd_df = pd.DataFrame({'macd_hist': hist})
    df = pd.concat([df, macd_df], axis=1)
    df['macd_hist_positive'] = df["macd_hist"].apply(lambda x: x > 0)
    df = add_status_boolean_change(df, 'macd_hist_positive')
    df = df.drop(['macd_hist', 'macd_hist_positive'], axis=1)
    return df


def add_rsi(df):
    # 終値の差分を計算する
    delta = df['Close'].diff()

    # 値上がり幅と値下がり幅をシリーズで計算する
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # 値上がり幅の移動平均と値下がり幅の移動平均を計算する
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    # RSIを計算する
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # データフレームにRSI列を追加する
    df['RSI'] = rsi
    df['RSI_3MA'] = df['RSI'].rolling(3).mean()
    df['RSI_3MA_diff'] = df['RSI_3MA'].diff()
    df['RSI_3MA_diff_positive'] = df["RSI_3MA_diff"].apply(lambda x: x > 0)

    return df


def add_status_boolean_change(df, col_name):
    df[f'{col_name}_shifted'] = df[col_name].shift()
    df.loc[(df[f'{col_name}_shifted'] == False) & (df[col_name] == True), f'transition_{col_name}'] = '好転'
    df.loc[(df[f'{col_name}_shifted'] == False) & (df[col_name] == False), f'transition_{col_name}'] = '悪継続'
    df.loc[(df[f'{col_name}_shifted'] == True) & (df[col_name] == True), f'transition_{col_name}'] = '良継続'
    df.loc[(df[f'{col_name}_shifted'] == True) & (df[col_name] == False), f'transition_{col_name}'] = '悪化'
    df = df.drop(f'{col_name}_shifted', axis=1)
    return df
