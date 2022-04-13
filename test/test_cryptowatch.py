import unittest
from app.tracker.cryptowatch import PricesFetcher


class TestPricesfetcher(unittest.TestCase):
	prices_fetcher = PricesFetcher()

	def test_price_datatype(self):
		"""Checking if the price return is a float"""
		price = self.prices_fetcher.get_prices('btceur')
		self.assertEqual(True, isinstance(price, float))


if __name__ == "__main__":
	unittest.main()
