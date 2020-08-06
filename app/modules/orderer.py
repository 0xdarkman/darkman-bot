from dataclasses import dataclass
from typing import Optional
from app.util.logger import Logger


logger = Logger("ORDERER")


@dataclass
class Orderer:
	status: Optional[str] = None
	stop_loss: int = 0
	open_price: Optional[float] = None
	close_price: Optional[float] = None

	def open(self, price):
		self.status = "OPENED"
		self.open_price = price
		return self

	def close(self, price):
		self.status = "CLOSED"
		self.close_price = price
		return self

	def get_profit(self):
		return self.close_price - self.open_price
