import time
from cryptowatch import PricesFetcher
from db import DBManager


def main():
    db_manager = DBManager('database', 'mcdata', 'mc_data_123', 'db', '5432')
    prices_fetcher = PricesFetcher()
    sync(db_manager, prices_fetcher)


def sync(db_manager: DBManager, prices_fetcher: PricesFetcher):
    pairs = prices_fetcher.get_pairs_static()

    while True:
        for pair in pairs:
            price = prices_fetcher.get_prices(pair)
            db_manager.insert_raw_crypto_pair_price_history(pair, price)

        records = db_manager.get_metrics()
        for record in records:
            pair = record[0]
            latest_price = record[1]
            weekly_average = record[2]
            min_price = record[3]
            max_price = record[4]
            std_rank = record[5]
            db_manager.insert_crypto_pair_metrics(pair, latest_price, weekly_average, min_price, max_price, std_rank)

        # Wait one hour
        time.sleep(3600)


if __name__ == '__main__':
    print('Starting app...')
    main()
