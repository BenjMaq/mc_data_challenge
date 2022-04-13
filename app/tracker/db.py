import sys
import datetime

from sqlalchemy import create_engine


class DBManager:

	def __init__(self, db_name, db_user, db_pw, db_host, db_port):
		self.db_name = db_name
		self.db_user = db_user
		self.db_pw = db_pw
		self.db_host = db_host
		self.db_port = db_port
		self.db_engine = self.build_db_engine()

	def build_db_engine(self):
		"""Build DB engine"""
		db_string = f'postgresql://{self.db_user}:{self.db_pw}@{self.db_host}:{self.db_port}/{self.db_name}'
		return create_engine(db_string)

	def insert_raw_crypto_pair_price_history(self, pair, price):
		"""Insert data into raw_crypto_pair_price_history"""
		insert = \
			f"INSERT INTO raw_crypto_pair_price_history (timestamp, pair, price) "+\
			f"VALUES ('{datetime.datetime.now()}', '{pair}', {price});"
		try:
			self.db_engine.execute(insert)
		except Exception as e:
			print(f'Error inserting records', e)
			sys.exit(-1)

	def insert_crypto_pair_metrics(self, pair, price, weekly_average, min_price, max_price, std_rank):
		"""Insert data into crypto_pair_metrics"""
		insert = \
			f"INSERT INTO crypto_pair_metrics (timestamp, pair, latest_price, weekly_average, min_price, max_price, std_rank) "+\
			f"VALUES ('{datetime.datetime.now()}', '{pair}', {price}, {weekly_average}, {min_price}, {max_price}, {std_rank});"
		try:
			self.db_engine.execute(insert)
		except Exception as e:
			print(f'Error inserting records', e)
			sys.exit(-1)

	def get_metrics(self):
		"""Compute metrics to enrich the table. Metrics computed are min_price, max_price, weekly_average and rank"""
		now = datetime.datetime.now()
		days_ago = now - datetime.timedelta(days=7)
		one_day_ago = now - datetime.timedelta(days=1)
		query = f"""
			WITH latest_timestamp AS (
				SELECT 
					pair,
					MAX(timestamp) AS latest_timestamp
				FROM raw_crypto_pair_price_history
				GROUP BY
					pair
			),
			latest_price AS (
			SELECT 
				rpph.pair,
				rpph.price
			FROM raw_crypto_pair_price_history rpph 
			LEFT JOIN latest_timestamp lt
				ON rpph.timestamp = lt.latest_timestamp
			),
			metrics as (
				SELECT 
					pair,
					sum(price) / count(1) as average,
					min(price) as min_price,
					max(price) as max_price
				FROM raw_crypto_pair_price_history
				WHERE 
					timestamp >= '{days_ago}'
				GROUP BY
					pair
			),
			stddev AS (
				SELECT
					pair, 
					STDDEV(price) AS std 
				FROM raw_crypto_pair_price_history 
				WHERE 
					timestamp > '{one_day_ago}'
				GROUP BY 
					pair
			),
			rank_stddev AS (
				SELECT
					pair, 
					RANK() OVER(ORDER BY std DESC) AS std_rank 
				FROM stddev
			)
			SELECT 
				lp.pair,
				lp.price,
				m.average,
				m.min_price,
				m.max_price,
				s.std_rank
			FROM latest_price lp
			LEFT JOIN metrics m
				ON lp.pair = m.pair
			LEFT JOIN rank_stddev s
				ON lp.pair = s.pair
		"""
		try:
			results = self.db_engine.execute(query)
			return results.fetchall()
		except Exception as e:
			print(f'Error computing metrics', e)
			sys.exit(-1)
