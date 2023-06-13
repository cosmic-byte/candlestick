## Candlestick
A prototype aggregator for stock prices. 

#### The service does the following:
- Receives price changes (quotes) for various stock (instruments) via websocket
- Aggregates these historic price data for each instrument
- Provides an endpoint for querying these data


### Notes
- This project is mostly for demonstrating the flexibility of clean architecture
- To actually view events, we'll need a separate service that publishes these stream of events via websocket


### Requirements
- python 3.10
- poetry
- Fast API

### Development setup
Please follow the steps synchronously

- build base image
```shell
make build-local-base
```

- build services
```shell
docker-compose build
```

- apply migrations
```shell
docker-compose run candlestick make db_upgrade
```

- To run tests (currently only infrastructure test is available)
First start the database
```shell
make start_db
```

Once db is started, run the test
```shell
docker-compose run candlestick make test
```

Start all the services (api, instrument-consumer and quote-consumer)
```shell
make start_infrastructure
```
To test or view the interactive API documentation, visit http://localhost:8081


### TODO
- Handle empty candles to use previous price quote
- Improve test coverage
- Proper exception handling
- General cleanup
- Optional --> scaling (Kubernetes)
