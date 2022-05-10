import random

from main import *
import pandas as pd


class Strategy(StrategyBase):
    def onData(self, snapshot, broker) -> None:
        if random.random() > 0.43:
            broker.addOrder(
                {"symbol": "AAPL", "quantity": 5, "orderType": "market"})
        else:
            broker.addOrder(
                {"symbol": "AAPL", "quantity": -5, "orderType": "market"})


if __name__ == "__main__":
    backtest = Backtest(Strategy("Test"), (datetime.datetime(2017, 5, 8), datetime.datetime(2022, 5, 6)),
                        Timeframe.DAILY)

    backtest.dataProvider.addDataSet("test", pd.read_csv("exampleData/AAPL.csv"))

    backtest.run()

