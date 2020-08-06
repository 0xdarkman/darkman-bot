from dataclasses import dataclass
from app.modules.orderer import Orderer
from typing import List, Optional


@dataclass
class Trader:
    num_orders: int = 1
    balance: int = 100
    order = Orderer()

    def trade(self, curr_price, trade_price):
        self.__open_order(curr_price=curr_price, trade_price=trade_price)
        self.__close_order(curr_price=curr_price, trade_price=trade_price)  # trade_price = row["ma"]
        self.__update_balance()

        return self

    def __open_order(self, curr_price, trade_price):
        if self.order.status != "OPENED" and (curr_price < trade_price):
            self.order.open(curr_price)

    def __close_order(self, curr_price, trade_price):
        if self.order.status == "OPENED" and curr_price > trade_price:
            self.order.close(curr_price)

    def __update_balance(self):
        if self.order.status == "CLOSED":
            self.balance += self.order.get_profit()
            self.order.status = ""


    # def __check_stop_loss(self, curr_price):
    #     for order in self.orders:
    #         if order.status == "OPEN":
    #             order.tick(curr_price)

