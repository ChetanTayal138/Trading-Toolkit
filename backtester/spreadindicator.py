import backtrader as bt



class SpreadIndicator(bt.Indicator):

	lines = ('spread', )

	
	def __init__(self, beta):

		self.beta = beta
		print(self.beta)
		print(self.data1)
		print(self.data0)

		spread = self.data1 - (self.beta * self.data0)
		print(spread)
		self.l.spread = spread
		print("Returning")
