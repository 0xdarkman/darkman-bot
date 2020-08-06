import pandas as pd

from dataclasses import dataclass
from app.modules.handlers import get_ma_indicator
from app.modules.trader import Trader
from app.settings.config import HIST_BTCUSD_4H_WEIGHTED_PKL
from app.util.df_utils import load_pickle, filter_frame_by_dt_range, change_col_type


@dataclass
class PipeSimpleMA:
    def __post_init__(self):
        self.trader = Trader()
        self.df = (
            load_pickle(file_path=HIST_BTCUSD_4H_WEIGHTED_PKL)
                .pipe(filter_frame_by_dt_range, start="2020-01-01", end="2020-04-01")
                .pipe(change_col_type, col="Weighted_Price", set_type="float")
                .pipe(get_ma_indicator)
                .pipe(self.__prepare_input)
                .pipe(self.__execute_trader, trader=self.trader)
        )

    @staticmethod
    def __prepare_input(df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns={"Weighted_Price": "curr_price", "MA_15": "ma"})



    @staticmethod
    def __execute_trader(df: pd.DataFrame, trader) -> pd.DataFrame:
        def get_trade(trader, row):
            return trader.trade(curr_price=row["curr_price"], trade_price=row["ma"])
        df["traded"] = df.apply(lambda row: get_trade(trader, row), axis=1)
        df['balance'] = df['traded'].apply(lambda x: x.balance)
        return df


if __name__ == '__main__':
    pipe = PipeSimpleMA()
    df = pipe.df
