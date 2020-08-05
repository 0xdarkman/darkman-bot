import pandas as pd


class Indicator:
	def __init__(self):
		pass

	@staticmethod
	def ma(df, col, n):
		MA = pd.Series(df[col].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
		df = df.join(MA)
		return df
