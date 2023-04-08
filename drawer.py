import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib


def pair(df):
    print(df.columns)
    # print('drawer')
    # 'Close', 'macd_hist_positive', 'transition_macd_hist_positive', 'RSI',
    # 'RSI_3MA', 'RSI_3MA_diff', 'RSI_3MA_diff_positive',
    # 'signal_macd_rsi_positive', 'stoch_k', 'stoch_d', 'signal_stoch_d',
    # 'slow_stoch_d', 'signal_slow_stoch_d', 'gdx_stoch',
    # 'transition_gdx_stoch', 'mean_3', 'mean_5', 'mean_7'],
    sns.barplot(x='mean_7', y='signal_gd_macd_rsi_positive', data=df)
    plt.tight_layout()
    plt.show()


def extract(df):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
    df = df.loc[df["transition_golden_cross"] == '好転']
    # df = df.loc[df["transition_gdx_stoch"] == '好転']
    df = df.loc[df["transition_macd_hist_positive"] == '好転']
    # df = df.loc[df["signal_macd_rsi_positive"] == True]
    # df = df.loc[df["transition_gdx_stoch"] == '好転']

    sns.histplot(ax=axes[0, 0], data=df, x='mean_2')
    sns.histplot(ax=axes[0, 1], data=df, x='mean_4')
    sns.histplot(ax=axes[0, 2], data=df, x='mean_6')
    sns.countplot(ax=axes[1, 0], data=df, x='positive_mean_2')
    sns.countplot(ax=axes[1, 1], data=df, x='positive_mean_4')
    sns.countplot(ax=axes[1, 2], data=df, x='positive_mean_6')
    plt.tight_layout()
    plt.show()
    # print(df)
