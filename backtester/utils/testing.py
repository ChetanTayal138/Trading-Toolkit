import os
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.append("../../quant")

from cointegration import cointegration_test
from alphabeta_regression import normal_equation
from stationarity import stationarity_test


class TestStatistics(unittest.TestCase):

	def test_stationarity(self):
		T = 1000
		A = np.random.normal(0,1,T)
		B = pd.Series(index=range(T))
		for i in range(T):
			B[i] = np.random.normal(i * 0.1, 1)
		B = B.values
		
		self.assertLessEqual(stationarity_test(A), 0.05)
		self.assertGreaterEqual(stationarity_test(B),0.05)

	def test_cointegration(self):
		N = 1000
		X1 = np.cumsum(np.random.normal(0,1,N))
		X2 = X1 + np.random.normal(0,1,N)
		X3 = np.random.normal(0,1,N)

		self.assertLessEqual(cointegration_test(X1, X2), 0.05)
		self.assertGreaterEqual(cointegration_test(X1, X3), 0.05)

	def test_regression(self):
		X1 = np.random.normal(0,1,100)
		X2 = 5 * X1 - 3

		self.assertAlmostEqual(normal_equation(X1.reshape(-1,1),X2)[0], -3)
		self.assertAlmostEqual(normal_equation(X1.reshape(-1,1),X2)[1], 5)

