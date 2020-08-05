import pandas as pd

from app.settings.config import HIST_BTCUSD_1M_CSV, HIST_BTCUSD_4H_WEIGHTED_PKL


df = pd.read_csv(HIST_BTCUSD_1M_CSV)
df.Timestamp = pd.to_datetime(df.Timestamp, unit='s')
df.index = df.Timestamp
df = df.resample('4H').mean()
df = df.drop_duplicates(keep='first')
df = df.reset_index()
df = df.rename(columns={"Timestamp": "Date"})
df = df[["Date", "High", "Low", "Open", "Close", "Weighted_Price"]]
df.to_pickle(HIST_BTCUSD_4H_WEIGHTED_PKL)
