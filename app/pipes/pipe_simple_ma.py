import pandas as pd

from dataclasses import dataclass
from app.modules.handlers import get_ma_indicator
from app.modules.trader import Trader
from app.settings.config import HIST_BTCUSD_4H_WEIGHTED_PKL
from app.util.df_utils import load_pickle, filter_frame_by_dt_range, change_col_type
from app.modules.plotter import Plotter

@dataclass
class PipeSimpleMA:
    def __post_init__(self):
        self.trader = Trader()
        self.df = (
            load_pickle(file_path=HIST_BTCUSD_4H_WEIGHTED_PKL)
                .pipe(filter_frame_by_dt_range, start="2019-01-01", end="2020-04-01")
                .pipe(change_col_type, col="Weighted_Price", set_type="float")
                .pipe(get_ma_indicator)
                .pipe(self.__prepare_input)
                .pipe(self.__preprocess)
                .pipe(self.__execute_trader, trader=self.trader)
                .pipe(self.__postprocess)
        )

    @staticmethod
    def __prepare_input(df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns={"Weighted_Price": "curr_price", "MA_15": "ma"})

    @staticmethod
    def __preprocess(df: pd.DataFrame) -> pd.DataFrame:
        df["pct_change"] = df["curr_price"].pct_change()
        return df

    @staticmethod
    def __execute_trader(df: pd.DataFrame, trader) -> pd.DataFrame:
        def get_trade(trader, row):
            trader.trade(curr_price=row["curr_price"], trade_price=row["ma"], pct_change=row["pct_change"])
            row["balance"] = trader.balance
            row["active"] = trader.order.active
            return row
        df = df.apply(lambda row: get_trade(trader, row), axis=1)
        return df

    @staticmethod
    def __postprocess(df: pd.DataFrame) -> pd.DataFrame:
        df = df.set_index("Date")
        df["active"] = df["active"].apply(lambda x: 1 if x is True else 0)
        return df

    def plot_frame(self, df: pd.DataFrame) -> pd.DataFrame:
        Plotter(df)

if __name__ == '__main__':
    pipe = PipeSimpleMA()
    df = pipe.df
    Plotter(df)
