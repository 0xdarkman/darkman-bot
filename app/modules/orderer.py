from app.modules.logger import Logger


class Orderer(object):
	def __init__(self, currentPrice, stopLoss=0):
		self.output = Logger()
		self.status = "OPEN"
		self.entryPrice = currentPrice
		self.exitPrice = ""
		self.output.log("Order opened")
		if stopLoss:
			self.stopLoss = currentPrice - stopLoss
	
	def close(self, currentPrice):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.output.log("Order closed")

	def tick(self, currentPrice):
		if self.stopLoss:
			if currentPrice < self.stopLoss:
				self.close(currentPrice)

	def show_order(self):
		order_status = "Entry Price: "+str(self.entryPrice)+" Status: "+str(self.status)+" Exit Price: "+str(self.exitPrice)

		if self.status == "CLOSED":
			order_status = order_status + " Profit: "
			if self.exitPrice > self.entryPrice:
				order_status = order_status + "\033[92m"
			else:
				order_status = order_status + "\033[91m"

			order_status = order_status+str(self.exitPrice - self.entryPrice)+"\033[0m"

		self.output.log(order_status)
