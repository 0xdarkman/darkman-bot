from dataclasses import dataclass
from app.modules.orderer import Orderer
from typing import List, Optional


@dataclass
class StrategyBase:
    rr: Optional[float] = 0.1
    fee: Optional[float] = 0.002
    num_orders: int = 1
    balance: int = 1
    order = Orderer()

    def trade(self, curr_price, trade_price, pct_change):
        self.__open_order(curr_price=curr_price, trade_price=trade_price)
        self.__close_order(curr_price=curr_price, trade_price=trade_price, pct_change=pct_change)  # trade_price = row["ma"]
        return self

    def __open_order(self, curr_price, trade_price):
        if not self.order.active and (curr_price < trade_price):
            self.order.open(curr_price)

    def __close_order(self, curr_price, trade_price, pct_change):
        if self.order.active and (pct_change < -0.05 or curr_price > trade_price):
            self.order.close(curr_price)
            self.__update_balance()

    def __get_profit(self):
        return (self.rr * self.balance * (self.order.close_price - self.order.open_price)) / self.order.close_price

    def __update_balance(self):
        self.balance += self.__get_profit() * (1-self.fee)

    # def __check_stop_loss(self, curr_price):
    #     for order in self.orders:
    #         if order.status == "OPEN":
    #             order.tick(curr_price)

