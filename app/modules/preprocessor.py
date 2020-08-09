import pandas as pd

from app.settings.config import HIST_BTCUSD_1M_CSV, HIST_BTCUSD_1H_OHLC_PKL


df = pd.read_csv(HIST_BTCUSD_1M_CSV)
df.Timestamp = pd.to_datetime(df.Timestamp, unit='s')
df.index = df.Timestamp
df = df.resample('1H').mean()
df = df.drop_duplicates(keep='first')
df = df.reset_index()
df = df.rename(columns={"Timestamp": "Date"})
# df = df[["Date", "High", "Low", "Open", "Close", "Weighted_Price"]]
df = df.rename(columns={'Volume_(Currency)': 'Volume', 'Weighted_Price': 'Price_Average'})
cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Price_Average']
df = df[cols]
df.to_pickle(HIST_BTCUSD_1H_OHLC_PKL)
