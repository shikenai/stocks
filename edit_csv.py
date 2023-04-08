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
    if 'macd_hist_positive' in df.columns and 'RSI_3MA_diff_positive' in df.columns:
        df['signal_macd_rsi_positive'] = (df['macd_hist_positive'] & df['RSI_3MA_diff_positive'])
    df = add_stochastics(df)
    mean_list = [3, 5, 7]
    for i in mean_list:
        df[f'mean_{str(i)}'] = df['Close'].rolling(i).mean().shift(-(i-1))/df['Close']
    df = df.drop(['Date', 'Volume', 'Open', 'High', 'Low'], axis=1)
    print(df)
    return df


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

    macd_df = pd.DataFrame({'macd_hist': hist})
    df = pd.concat([df, macd_df], axis=1)
    # macd_histの正負判定を行う
    df['macd_hist_positive'] = df["macd_hist"].apply(lambda x: x > 0)
    df = add_status_boolean_change(df, 'macd_hist_positive')
    df = df.drop(['macd_hist'], axis=1)
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
    # RSIの今後三日間の平均をとる
    df['RSI_3MA'] = df['RSI'].rolling(3).mean()
    # RSIの今後三日間の平均の差分を取る
    df['RSI_3MA_diff'] = df['RSI_3MA'].diff()
    # RSIの今後三日間の平均の差分を取り、正負判定を行う
    # 正の場合、RSIが上昇傾向にあると判断できる（と思われる）
    df['RSI_3MA_diff_positive'] = df["RSI_3MA_diff"].apply(lambda x: x > 0)

    return df


def add_status_boolean_change(df, col_name):
    # booleanデータの前後関係から、現在の状態を判定する
    df[f'{col_name}_shifted'] = df[col_name].shift()
    df.loc[(df[f'{col_name}_shifted'] == False) & (df[col_name] == True), f'transition_{col_name}'] = '好転'
    df.loc[(df[f'{col_name}_shifted'] == False) & (df[col_name] == False), f'transition_{col_name}'] = '悪継続'
    df.loc[(df[f'{col_name}_shifted'] == True) & (df[col_name] == True), f'transition_{col_name}'] = '良継続'
    df.loc[(df[f'{col_name}_shifted'] == True) & (df[col_name] == False), f'transition_{col_name}'] = '悪化'
    df = df.drop(f'{col_name}_shifted', axis=1)
    return df


def add_stochastics(df, n=9, d_n=3):
    # 高値・安値のn日最大値・最小値を計算
    df['high_n'] = df['High'].rolling(n).max()
    df['low_n'] = df['Low'].rolling(n).min()

    # %Kを計算
    df['stoch_k'] = 100 * (df['Close'] - df['low_n']) / (df['high_n'] - df['low_n'])

    # %Dを計算
    df['stoch_d'] = df['stoch_k'].rolling(d_n).mean()
    df['signal_stoch_d'] = df['stoch_d'].apply(lambda x: 'Sell' if x >= 80 else 'Buy' if x <= 20 else 'stay')

    # slow%Dを計算
    df['slow_stoch_d'] = df['stoch_d'].rolling(d_n).mean()
    df['signal_slow_stoch_d'] = df['slow_stoch_d'].apply(lambda x: 'Sell' if x >= 80 else 'Buy' if x <= 20 else 'stay')

    # ゴールデンクロス判断
    df['gdx_stoch'] = df['stoch_d'] - df['slow_stoch_d'] > 0
    df = add_status_boolean_change(df, 'gdx_stoch')

    # 不要なカラムを削除
    df = df.drop(['high_n', 'low_n'], axis=1)

    return df
