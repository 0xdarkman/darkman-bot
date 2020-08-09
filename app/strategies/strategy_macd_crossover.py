import numpy as np
from dataclasses import dataclass
from app.modules.orderer import Orderer
from typing import List, Optional


@dataclass
class StrategyMacdCrossover:
    rr: Optional[float] = 0.1
    fee: Optional[float] = 0.002
    num_orders: int = 1
    balance: int = 1
    order = Orderer()

    def trade(self, row):
        self.__open_order(curr_price=row['curr_price'], row=row)
        self.__close_order(curr_price=row['curr_price'], row=row)
        return self

    def __open_order(self, curr_price, row):
        if not self.order.active:
            if row['cross'] == 1 and row['close'] > row['ema_200'] and row['macd'] < 0:
                self.order.open(curr_price)

    def __close_order(self, curr_price, row):
        if self.order.active:
            if row['cross'] == -1 and row['close'] < row['ema_200'] and row['macd'] > 0:
                self.order.close(curr_price)
                self.__update_balance()

    def __get_profit(self):
        return (self.rr * self.balance * (self.order.close_price - self.order.open_price)) / self.order.close_price

    def __update_balance(self):
        self.balance += self.__get_profit() * (1-self.fee)
