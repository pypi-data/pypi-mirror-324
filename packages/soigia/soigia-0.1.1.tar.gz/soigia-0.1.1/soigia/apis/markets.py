import ccxt
from soigia.env import config
from pandas import DataFrame


def connector(exchange="binanceusdm") -> ccxt.Exchange:
    if exchange not in ccxt.exchanges:
        raise ValueError("exhcange not found")

    conf = config.get(exchange, {})

    if exchange == "binance":
        return ccxt.binance(config=conf)
    if exchange == "binanceusdm":
        return ccxt.binanceusdm(config=conf)
    if exchange == "bybit":
        return ccxt.bybit(config=conf)
    if exchange == "bingx":
        return ccxt.bingx(config=conf)
    return ccxt.Exchange(config=conf)


class Exchange:
    def __init__(self, exchange='binanceusdm'):
        self.api = connector(exchange)

    def backtesting_dataframe(self, symbol, ohlcv=[]) -> DataFrame:
        df = DataFrame(ohlcv)
        df['symbol'] = symbol
        return df
