import pandas as pd
import matplotlib.pyplot as plt
from pykrx import stock
from datetime import datetime, timedelta


def get_stock_data(stock_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    df = stock.get_market_ohlcv(start_date, end_date, stock_code)

    # add index column to df['date'] first row
    df.insert(0, 'date', df.index)

    # change column name to date, open, high, low, close, volume, change
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'change']

    # remove index
    df = df.reset_index(drop=True)

    return df


def add_moving_avg_column(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df[f'moving_avg_{window}d'] = df['close'].rolling(window=window).mean()
    return df


def save_df_to_plot(df: pd.DataFrame, product_name: str, date: str):
    plt.figure(figsize=(30, 10))
    plt.plot(df['moving_avg_20d'], label='moving_avg_20d')
    plt.plot(df['moving_avg_60d'], label='moving_avg_60d')
    plt.xlabel('date')
    plt.xticks(rotation=90)
    plt.legend()
    
    plt.savefig(f'{date}_{product_name}.png')


if __name__ == "__main__":
    PRODUCT_CODES = ["005930", "000660", "035420"]

    # get today's date
    today = datetime.now().strftime("%Y%m%d")
    before_365_days = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")

    for product_code in PRODUCT_CODES:
        df = get_stock_data(product_code, before_365_days, today)
        df = add_moving_avg_column(df, 20)
        df = add_moving_avg_column(df, 60)
        df = df.dropna()
        save_df_to_plot(df, product_code, today)

