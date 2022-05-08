from main import *
import pandas as pd


class Strategy(StrategyBase):
    def onData(self, data: pd.DataFrame, broker: Broker) -> None:
        print(broker.balance, data)


if __name__ == "__main__":
    backtest = Backtest(Strategy("Test"), (datetime.datetime(2018, 1, 1), datetime.datetime(2018, 1, 5)),
                        Timeframe.DAILY)

    backtest.dataProvider.addDataSet("test", pd.read_csv("exampleData/AAPL.csv"))

    backtest.run()
    backtest.results()
