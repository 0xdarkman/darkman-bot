import numpy as np
from dataclasses import dataclass
from app.modules.orderer import Orderer
from typing import List, Optional


@dataclass
class StrategySimple:
    rr: Optional[float] = 0.1
    fee: Optional[float] = 0.002
    num_orders: int = 1
    balance: int = 1
    order = Orderer()

    def trade(self, row):
        self.__open_order(curr_price=row['curr_price'], signal=row['signal'])
        self.__close_order(curr_price=row['curr_price'], signal=row['signal'])
        return self

    def __open_order(self, curr_price, signal):
        if not self.order.active and signal == 1:
            self.order.open(curr_price)

    def __close_order(self, curr_price, signal):
        if self.order.active and (signal not in [1, np.nan, None, 0]):
            self.order.close(curr_price)
            self.__update_balance()

    def __get_profit(self):
        return (self.rr * self.balance * (self.order.close_price - self.order.open_price)) / self.order.close_price

    def __update_balance(self):
        self.balance += self.__get_profit() * (1-self.fee)
