import pandas as pd
import talib
import ta
import time


class Indicator:
	def __init__(self):
		pass

	@staticmethod
	def ma(df, col, n):
		MA = pd.Series(df[col].rolling(n, min_periods=n).mean(), name='MA_' + str(n))
		df = df.join(MA)
		return df

	def indicators(self, df):
		# Simple Moving Average (SMA)
		period = 30
		df['SMA_close'] = talib.SMA(df["close"], timeperiod=period)

		# Stochastic Oscillator (SO)
		period = 14
		sma_period = 3
		StochasticOscillator = ta.momentum.StochasticOscillator(high=df["high"], low=df["low"], close=df["close"],
																n=period, d_n=sma_period, fillna=False)
		df['SO'] = StochasticOscillator.stoch()

		# Momentum (M)
		period = 3
		df['Momentum'] = talib.MOM(df["close"], timeperiod=period)

		# Price Rate Of Change (ROC)
		'''
		Description:
		is a pure momentum oscillator that measures the percent change in price from one period to the next
		The ROC calculation compares the current price with the price “n” periods ago
		'''
		period = 12
		RateOfChange = ta.momentum.ROCIndicator(close=df["close"], n=period, fillna=False)
		df['ROC'] = RateOfChange.roc()

		# Williams %R
		'''
		Description:
		Williams %R reflects the level of the close relative to the highest high for the look-back period
        Williams %R oscillates from 0 to -100.
        Readings from 0 to -20 are considered overbought. Readings from -80 to -100 are considered oversold.
        '''
		lookback_period = 14
		WilliamsR = ta.momentum.WilliamsRIndicator(high=df["high"], low=df["low"], close=df["close"],
												   lbp=lookback_period, fillna=False)
		df['WR'] = WilliamsR.wr()

		# Weighted Closing Price (WCP)
		df['WCP'] = talib.WCLPRICE(df["high"], df["low"], df["close"])

		# Williams Accumulation Distribution Line
		# AKA Accumulation/Distribution Index (ADI)????
		'''
        Description:
        a volume-based indicator designed to measure the cumulative flow of money into and out of a security
        The Accumulation Distribution Line rises when the multiplier is positive and falls when the multiplier is negative.
        '''
		ADI = ta.volume.AccDistIndexIndicator(high=df["high"], low=df["low"], close=df["close"], volume=df["volume"],
											  fillna=False)
		df['ADI'] = ADI.acc_dist_index()

		# Moving Average Convergence Divergence (MACD)
		'''
        Description:
        Is a trend-following momentum indicator that shows the relationship between two moving averages of prices.
        '''
		period_longterm = 26
		period_shortterm = 12
		period_to_signal = 9
		MACD = ta.trend.MACD(close=df["close"], n_slow=period_longterm, n_fast=period_shortterm,
							 n_sign=period_to_signal, fillna=False)
		df['MACD'] = MACD.macd()

		start_time = time.time()
		# Commodity Channel Index (CCI)
		'''
        Description:
        CCI measures the difference between a security’s price change and its average price change. 
        high positive readings indicate that prices are well above their average, which is a show of strength. 
        low negative readings indicate that prices are well below their average, which is a show of weakness.
        '''
		periods = 20
		constant = 0.015
		# CCI = ta.trend.cci(high=df["high"], low=df["low"], close=df["close"], n=periods, c=constant, fillna=False)
		# df['CCI'] = CCI

		# Bollinger Bands (BB)
		'''
        Description:
        CCI measures the difference between a security’s price change and its average price change. 
        high positive readings indicate that prices are well above their average, which is a show of strength. 
        low negative readings indicate that prices are well below their average, which is a show of weakness.
        '''
		periods = 20
		n_factor_standard_dev = 2
		indicator_bb = ta.volatility.BollingerBands(close=df["close"], n=periods, ndev=n_factor_standard_dev,
													fillna=False)
		# Add Bollinger Bands features
		# df['bb_bbm'] = indicator_bb.bollinger_mavg()
		df['BB_H'] = indicator_bb.bollinger_hband()
		df['BB_L'] = indicator_bb.bollinger_lband()

		# Add Bollinger Band high indicator
		df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

		# Add Bollinger Band low indicator
		df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

		# Add width size Bollinger Bands
		df['bb_bbw'] = indicator_bb.bollinger_wband()
		# Mean open & close (M_O, M_C)
		period = 3
		df['MEAN_O_C'] = (talib.SMA(df["open"], timeperiod=period) / 2) + (
				talib.SMA(df["close"], timeperiod=period) / 2)

		# Variance open & close
		df["VAR_close"] = talib.VAR(df["close"], timeperiod=5, nbdev=1)
		df["VAR_open"] = talib.VAR(df["open"], timeperiod=5, nbdev=1)

		# high Price Average
		'''
        Description:
        Simple moving average over the high
        '''
		period = 3
		df['SMA_high'] = talib.SMA(df["high"], timeperiod=period)
		# low Price Average
		'''
        Description:
        Simple moving average over the low
        '''
		period = 3
		df['SMA_low'] = talib.SMA(df["low"], timeperiod=period)
		start_time = time.time()
		# high, low Average
		'''
        Description:
        Simple moving average over the sum of high and low
        '''
		period = 3
		df['SMA_H+L'] = talib.SMA(df["high"] + df["low"], timeperiod=period)

		# Trading Day Price Average
		'''
        Description:
        Simple moving average over the sum of the open, high, low and close
        '''
		period = 3
		df['SMA_H+L+C+O'] = talib.SMA(df["high"] + df["low"] + df["open"] + df["close"], timeperiod=period)

		# From here on adding random indicators according to the ta-lib library
		# ######################## OVERLAP STUDIES ############################
		# Double Exponential Moving Average
		period = 30
		df['DEMA'] = talib.DEMA(df["close"], timeperiod=period)
		# Exponential Moving Average
		period = 30
		df['EMA'] = talib.EMA(df["close"], timeperiod=period)
		# HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
		df['HT_TRENDLINE'] = talib.HT_TRENDLINE(df["close"])
		# KAMA - Kaufman Adaptive Moving Average
		period = 30
		df['KAMA'] = talib.KAMA(df["close"], timeperiod=period)
		# MA - Moving average
		period = 30
		start_time = time.time()
		df['MA'] = talib.MA(df["close"], timeperiod=period, matype=0)
		# MIDPOINT - MidPoint over period
		period = 14
		df['MIDPOINT'] = talib.MIDPOINT(df["close"], timeperiod=period)
		# MIDPRICE - Midpoint Price over period
		period = 14
		df['MIDPOINT'] = talib.MIDPRICE(df["high"], df["low"], timeperiod=period)
		# SAR - Parabolic SAR
		df['SAR'] = talib.SAR(df["high"], df["low"], acceleration=0, maximum=0)
		# SAREXT - Parabolic SAR - Extended
		df['SAREXT'] = talib.SAREXT(df["high"], df["low"], startvalue=0, offsetonreverse=0, accelerationinitlong=0,
									accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0,
									accelerationshort=0, accelerationmaxshort=0)
		# T3 - Triple Exponential Moving Average (T3)
		period = 5
		df['T3'] = talib.T3(df["close"], timeperiod=period, vfactor=0)
		# TEMA - Triple Exponential Moving Average
		period = 30
		df['TEMA'] = talib.TEMA(df["close"], timeperiod=period)
		# TRIMA - Triangular Moving Average
		period = 30
		df['TRIMA'] = talib.TRIMA(df["close"], timeperiod=period)
		# WMA - Weighted Moving Average
		period = 30
		df['WMA'] = talib.WMA(df["close"], timeperiod=period)

		# ######################## Momentum Indicators ############################
		# ADX - Average Directional Movement Index
		period = 14
		df['ADX'] = talib.ADX(df["high"], df["low"], df["close"], timeperiod=period)
		# ADXR - Average Directional Movement Index Rating
		period = 14
		df['ADXR'] = talib.ADXR(df["high"], df["low"], df["close"], timeperiod=period)

		start_time = time.time()
		# APO - Absolute Price Oscillator
		df['APO'] = talib.APO(df["close"], fastperiod=12, slowperiod=26, matype=0)
		# AROON - Aroon
		df['aroondown'], df['aroonup'] = talib.AROON(df["high"], df["low"], timeperiod=14)
		# AROONOSC - Aroon Oscillator
		period = 14
		df['AROONOSC'] = talib.AROONOSC(df["high"], df["low"], timeperiod=14)
		# BOP - Balance Of Power
		period = 14
		df['BOP'] = talib.BOP(df["open"], df["high"], df["low"], df["close"])
		# CMO - Chande Momentum Oscillator
		df['CMO'] = talib.CMO(df["close"], timeperiod=14)
		# DX - Directional Movement Index
		df['DX'] = talib.DX(df["high"], df["low"], df["close"], timeperiod=14)
		# MFI - Money Flow Index
		df['MFI'] = talib.MFI(df["high"], df["low"], df["close"], df["volume"], timeperiod=14)
		# MINUS_DI - Minus Directional Indicator
		df['MINUS_DI'] = talib.MINUS_DI(df["high"], df["low"], df["close"], timeperiod=14)
		# MINUS_DM - Minus Directional Movement
		df['MINUS_DM'] = talib.MINUS_DM(df["high"], df["low"], timeperiod=14)
		# PLUS_DI - Plus Directional Indicator
		df['PLUS_DI'] = talib.PLUS_DI(df["high"], df["low"], df["close"], timeperiod=14)
		# PLUS_DM - Plus Directional Movement
		df['PLUS_DM'] = talib.PLUS_DM(df["high"], df["low"], timeperiod=14)
		# PPO - Percentage Price Oscillator
		df['PPO'] = talib.PPO(df["close"], fastperiod=12, slowperiod=26, matype=0)
		# ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
		df['ROCP'] = talib.ROCP(df["close"], timeperiod=10)
		# ROCR - Rate of change ratio: (price/prevPrice)
		df['ROCR'] = talib.ROCR(df["close"], timeperiod=10)
		# ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
		df['ROCR100'] = talib.ROCR100(df["close"], timeperiod=10)
		# RSI - Relative Strength Index
		df['RSI'] = talib.RSI(df["close"], timeperiod=14)
		# TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
		df['TRIX'] = talib.TRIX(df["close"], timeperiod=30)
		# ULTOSC - Ultimate Oscillator
		df['ULTOSC'] = talib.ULTOSC(df["high"], df["low"], df["close"], timeperiod1=7, timeperiod2=14, timeperiod3=28)

		# ######################## volume Indicators ############################
		# AD - Chaikin A/D Line
		df['AD'] = talib.AD(df["high"], df["low"], df["close"], df["volume"])
		# ADOSC - Chaikin A/D Oscillator
		df['ADOSC'] = talib.ADOSC(df["high"], df["low"], df["close"], df["volume"], fastperiod=3, slowperiod=10)
		# OBV - On Balance volume
		df['OBV'] = talib.OBV(df["close"], df["volume"])

		# ######################## Cycle Indicators ############################
		# HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
		df['HT_DCPERIOD'] = talib.HT_DCPERIOD(df["close"])
		# HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase

		# df['HT_DCPHASE'] = talib.HT_DCPHASE(df["close"])

		# HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
		# df['HT_TRENDMODE'] = talib.HT_TRENDMODE(df["close"])

		# ######################## Price transform functions ############################
		# AVGPRICE - Average Price
		df['AVGPRICE'] = talib.AVGPRICE(df["open"], df["high"], df["low"], df["close"])
		# MEDPRICE - Median Price
		df['MEDPRICE'] = talib.MEDPRICE(df["high"], df["low"])
		# TYPPRICE - Typical Price
		df['TYPPRICE'] = talib.TYPPRICE(df["high"], df["low"], df["close"])
		# WCLPRICE - Weighted close Price
		df['WCLPRICE'] = talib.WCLPRICE(df["high"], df["low"], df["close"])

		# ################################ END OF TECHINCAL INDICATORS #########################
		return df