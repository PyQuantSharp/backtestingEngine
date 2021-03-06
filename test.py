import random

from main import *
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class Strategy(StrategyBase):
    def __init__(self, strategy_name: str):
        self.x = False

    def onData(self, snapshot, broker) -> None:
        tickers = broker.getTickers(snapshot["time"])
        for ticker in tickers:
            broker.addOrder({
                "ticker": ticker,
                "quantity": 1,
                "orderType": "market",
                "dataset": "spy_options_eod",
            }, snapshot)
            self.x = True


if __name__ == "__main__":
    backtest = Backtest(Strategy("Test"), (datetime.datetime(2020, 9, 16, 2, 0), datetime.datetime(2020, 9, 19)),
                        Timeframe.DAILY)

    backtest.dataProvider.addDataset({
        "name": "SPY",
        "source": "File",
        "set": "C:\\Development\\Trading\\dataDownload\\dataCache\\SPY-equity.csv",
    })

    backtest.dataProvider.addDataset({
        "name": "spy_options_eod",
        "source": "Database",
        "set": "spy_options_eod",
        "type": "options",
    })

    backtest.dataProvider.addDataset({
        "name": "aapl",
        "source": "Database",
        "set": "aapl_daily",
        "type": "equity",
    })

    backtest.run()
