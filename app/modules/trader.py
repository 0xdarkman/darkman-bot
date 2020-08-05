from dataclasses import dataclass
from app.modules.orderer import Orderer
from typing import List

@dataclass
class Trader:
    num_orders: int = 1

    def __post_init__(self):
        self.orders = []

    def manage_orders(self, curr_price, trade_price):
        self.orders = self.get_open_orders()
        print(self.orders)
        self.__close_order(curr_price, trade_price)  # trade_price = row["ma"]
        self.__open_order(curr_price, self.orders, self.num_orders, trade_price)
        self.__update_open_orders(curr_price)
        # self.__show_positions()

    def __close_order(self, curr_price, trade_price):
        [order.close(curr_price) if curr_price > trade_price else order for order in self.orders]

    def __open_order(self, curr_price, orders, num_orders, trade_price):
        if (len(orders) < num_orders) & (curr_price < trade_price):
            self.orders.append(Orderer(curr_price, stopLoss=.0001))

    def __update_open_orders(self, curr_price):
        for order in self.orders:
            if order.status == "OPEN":
                order.tick(curr_price)

    def __show_positions(self):
        for order in self.orders:
            order.show_order()

    def get_open_orders(self):
        return list(filter(lambda x: x.status == "OPEN", self.orders))
