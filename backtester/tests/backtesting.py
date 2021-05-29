import unittest
import sys
sys.path.append(r"..\engine")
from buy_hold import strat_BuyHold

class TestBuyHold(unittest.TestCase):

	def test_strategy(self):
		self.assertAlmostEqual(strat_BuyHold(10000),103980.7705)

