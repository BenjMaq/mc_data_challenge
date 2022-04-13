CREATE TABLE IF NOT EXISTS raw_crypto_pair_price_history (
    timestamp TIMESTAMP,
    pair VARCHAR,
    price FLOAT
);

CREATE TABLE IF NOT EXISTS crypto_pair_metrics (
    timestamp TIMESTAMP,
    pair VARCHAR,
    latest_price FLOAT,
    weekly_average FLOAT,
    min_price FLOAT,
    max_price FLOAT,
    std_rank INT
);