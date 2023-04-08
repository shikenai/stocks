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
    sns.barplot(x='mean_3', y='signal_gd_macd_rsi_positive', data=df)
    plt.show()
