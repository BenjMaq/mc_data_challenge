import requests
import sys


class PricesFetcher:

	def __init__(self):
		self.base_url = 'https://api.cryptowat.ch'

	def get_pairs_static(self) -> list:
		"""
		Return 10 static pairs that are available in the Kraken market.
		"""
		static_pairs = [
			'btceur', 'btcusd', 'etheur', 'ltceur', 'solusd', 'xrpusd', 'adaeur', 'waveseur', 'bateth', 'dogeusd'
		]
		return static_pairs

	def get_prices(self, pair: str, market: str = 'kraken') -> float:
		"""
		Takes a pair and a market as input and returns the price of the pair if it exists in the market.
		Default market is 'kraken'.
		"""
		method = f'/markets/{market}/{pair}/price'
		r = requests.get(self.base_url + method)
		if 'result' in r.json():
			return r.json()['result']['price']
		else:
			print(f'The pair {pair} and/or market {market} cannot be found. Please make sure you only use valid pair/market')
			sys.exit(-1)
