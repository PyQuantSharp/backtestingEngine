import random

from main import *
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class Strategy(StrategyBase):

    def onData(self, snapshot, broker) -> None:
        tickers = broker.getTickers(snapshot["time"])

        broker.addOrder({
            "ticker": tickers[random.randint(0, len(tickers) - 1)],
            "quantity": random.randint(1, 10),
            "orderType": "market",
            "dataset": "spy_options_eod",
        }, snapshot)
        print(snapshot["time"])


if __name__ == "__main__":
    backtest = Backtest(Strategy("Test"), (datetime.datetime(2020, 8, 2), datetime.datetime(2030, 5, 6)),
                        Timeframe.DAILY)

    backtest.dataProvider.addDataset({
        "name": "spy",
        "source": "File",
        "set": "C:\\Development\\Trading\\dataDownload\\dataCache\\SPY-equity.csv",
    })

    backtest.dataProvider.addDataset({
        "name": "spy_options_eod",
        "source": "Database",
        "set": "spy_options_eod",
        "type": "options",
        "underlying": "spy"
    })

    backtest.dataProvider.addDataset({
        "name": "aapl",
        "source": "Database",
        "set": "aapl_daily",
        "type": "equity",
    })

    backtest.run()
