import unittest
import sys

from buy_hold import strat_BuyHold

class TestBuyHold(unittest.TestCase):

	def test_strategy(self):
		self.assertAlmostEqual(strat_BuyHold(10000),13980.7705)
		
	def test_no_capital(self):
		self.assertAlmostEqual(strat_BuyHold(0),0)
		