import random

from main import *
import pandas as pd


class Strategy(StrategyBase):

    def onData(self, snapshot, broker) -> None:
        if random.random() > 0.43:
            broker.addOrder(
                {"ticker": "AAPL", "quantity": 5, "orderType": "market"}, snapshot)
        else:
            broker.addOrder(
                {"ticker": "AAPL", "quantity": -5, "orderType": "market"}, snapshot)


if __name__ == "__main__":
    backtest = Backtest(Strategy("Test"), (datetime.datetime(2015, 5, 8), datetime.datetime(2022, 5, 6)),
                        Timeframe.DAILY)

    backtest.dataProvider.addDataset({
        "name": "spy_options_eod",
        "source": "File",
        "set": "exampleData/spy_options_eod.csv",
    })

    backtest.dataProvider.addDataset({
        "name": "aapl_daily",
        "source": "Database",
        "set": "aapl_daily"
    })

    backtest.run()
