# MC Data - Data challenge

This application fetches prices from the Cryptowatch API, computes some metrics on these prices, and finally inserts these metrics into a PostgreSQL database.

**Disclaimer:** 

I've limited myself to a set of 10 pairs: 'btceur', 'btcusd', 'etheur', 'ltceur', 'solusd', 'xrpusd', 'adaeur', 'waveseur', 'bateth', 'dogeusd'. This has been done to be able to focus on the core part of the app. In production, we would need to decide if we want all pairs, or a specific set of pairs. The Cryptowatch API allows users to list all pairs and their associated markets. I would leverage this API for that purpose if required.

## Architecture

This application is maintained using docker. There are two services running: a database service and a python service.
- The python service fetches data from the Cryptowatch API and inserts the prices into the database. It also inserts the computed metrics back into another table for users to fetch.
- The database service stores the prices for the different crypto pairs and also their associated metrics. The database service is also used to compute metrics related to these pairs.

## How-to 
### Run the application

The application is built with Docker (get Docker [here](https://docs.docker.com/get-docker/)). To run the app, clone this repo and run `docker-compose up --build -d`.
This will create and run two containers:
- `app` container
- `database` container

The app container will start fetching prices as soon as it's started (and will do so every hour) and will load data into the database.

### Check metrics from the database

To check the metrics, you need to bash into the database container. To do so, run the below commands
- `docker ps` and grab the database container ID
- `docker exec -it <CONTAINER_ID> bash`

Once you're in the container, run
- `psql postgres://mcdata:mc_data_123@localhost:5432/database`
You can now check the metrics by running some SQL queries, e.g. get the latest weekly minimum price and rank of the `btceur` pair:
```
select pair, min_price, std_rank from crypto_pair_metrics where pair = 'btceur' order by timestamp desc limit 1;
```

### Run tests
There are a very limited number of unit tests. This is because most test required are integration tests and were not done due to limited time.

To run unit tests, first set-up the virtual environment `make setup-environment` and then you can run `make test`.

### Database schema
The different schemas can be found under database/create_table.sql

## Improvements
### Scalability 
- We might hit some rate-limiting issues when fetching all the market/pairs rather than just a set of them. 
- If I needed to sample the metrics more frequently/more metrics
  - Instead of fetching the price for each pair in sequence, I would use multiprocessing to fetch them in parallel.
  - I would leverage a queue-based service like Kafka to store each response instead of writing directly to the database. This would prevent losing data if there are a lot of writes or locks on the DB
  - Using Kafka to store messages would also mean we can use a stream-processing framework like Flink/Kafka streams/Spark streaming to compute aggregations in real-time and take read-time actions based on the computed metrics (e.g. trigger a buy action if price < threshold) 
  - With a lot of different pairs (billions), we might hit some scalability issues with a single database. To improve scalability, I would look into deploying the databases following a master-slave model, where only one database (master) would receive the writes and its replicas would serve the multiple reads from users. I would also shard my database (based on a hash of the pair, for example) so that it's faster to read and write.
  - Currently, metrics are computed using SQL. At scale, I would leverage parallelization, where each pair would be a key and assigned to a specific worker for metrics computation (mapreduce). It would help spread the load into multiple workers and prevent the same worker to crash from too much load. I could also use a MPP database to run SQL at scale, or a large scale data processing engine like Spark for computing metrics.
- I took the assumption that the latest price had to be used to compute all metrics. We could also take the decision to NOT recompute some metrics everytime (e.g. min_price, max_price, weekly_average). We could compute them once per day and store them in a different table (or cache) for easy and fast access when computing other metrics on the fly.
 
### Testing
- In production (and at larger scale), I would probably not leverage SQL for computing the different metrics. So, I would use unit tests for each metric to make sure the logic I implement is correct (test driven development)
- I would also leverage integration tests between the python service and the database service

### Production
- In production, I would leverage a cloud service for the database (e.g. AWS RDS). It would allow me to focus on the core logic of the app rather than focus on database management tasks such as backup, recovery, etc.
- I would setup a peer review process, where for each change to the code, a peer will have to review and approve the change.
- I would use a CI/CD tool like Jenkins or Buildkite to build the docker image and run continuous tests
- I would also use different environments like dev/stage/prod to test the application before going to production. I would deploy in these environments using GitOps and ArgoCD, for example.
- In production, I would probably run the app on Kubernetes to leverage auto-scaling and improve flexibility and scalability
- I would also manage secrets differently, via Kubernetes secrets or AWS SecretManager.

