from dataclasses import dataclass
from typing import Optional
from app.util.logger import Logger


logger = Logger("ORDERER")


@dataclass
class Orderer:
	active: Optional[bool] = None
	status: Optional[str] = None
	stop_loss: int = 0
	open_price: Optional[float] = None
	close_price: Optional[float] = None

	def open(self, price):
		self.open_price = price
		self.active = True
		return self

	def close(self, price):
		self.active = False
		self.close_price = price
		return self

