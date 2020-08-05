import pandas as pd
from app.modules.trader import Trader
from dataclasses import dataclass


@dataclass
class SimpleMAStrategy:
    df: pd.DataFrame
    num_orders: int = 1

    def __post_init__(self):
        df = self.df[["Weighted_Price", "MA_15"]]
        df = df.rename(columns={"Weighted_Price": "curr_price", "MA_15": "ma"})
        trader = Trader()
        df.apply(lambda row: trader.manage_orders(curr_price=row["curr_price"], trade_price=row["ma"]), axis=1)



