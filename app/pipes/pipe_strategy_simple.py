import numpy as np
import pandas as pd

from dataclasses import dataclass
from app.modules.handlers import get_ma_indicator
from app.strategies.strategy_simple import StrategySimple
from app.settings.config import HIST_BTCUSD_4H_WEIGHTED_PKL
from app.util.df_utils import load_pickle, filter_frame_by_dt_range, change_col_type, change_col_name
from app.modules.plotter import Plotter

@dataclass
class PipeSimpleMA:
    def __post_init__(self):
        self.df = (
            load_pickle(file_path=HIST_BTCUSD_4H_WEIGHTED_PKL)
                .pipe(filter_frame_by_dt_range, start="2019-01-01", end="2020-04-01")
                .pipe(change_col_type, col="Weighted_Price", set_type="float")
                .pipe(change_col_name, old_col="Weighted_Price", new_col="curr_price")
                .pipe(self.generate_signals)
                .pipe(self.apply_strategy)
                # .pipe(self.__postprocess)
                .pipe(self.plot_frame)
        )

    @staticmethod
    def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
        df = change_col_name(df, old_col="Close", new_col="close")

        short_window = 9
        long_window = 21

        df['long_short'] = 0
        df['short_mavg'] = df['close'].rolling(window=short_window, min_periods=1, center=False).mean()
        df['long_mavg'] = df['close'].rolling(window=long_window, min_periods=1, center=False).mean()
        df['long_short'][short_window:] = np.where(df['short_mavg'][short_window:] >= df['long_mavg'][short_window:], 1, 0)
        df['signal'] = df['long_short'].diff()
        return df

    @staticmethod
    def apply_strategy(df: pd.DataFrame) -> pd.DataFrame:
        def get_trade(trader, row):
            trader.trade(row)
            row["balance"] = trader.balance
            row["active"] = trader.order.active
            return row
        trader = StrategySimple()
        df = df.apply(lambda row: get_trade(trader, row), axis=1)
        return df

    @staticmethod
    def __postprocess(df: pd.DataFrame) -> pd.DataFrame:
        df["active"] = df["active"].apply(lambda x: 1 if x is True else 0)
        return df

    def plot_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        Plotter(df, plot_name="strategy_simple")
        return df


if __name__ == '__main__':
    pipe = PipeSimpleMA()
    df = pipe.df

