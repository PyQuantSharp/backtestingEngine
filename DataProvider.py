import pandas as pd
from matplotlib import pyplot as plt

from DbConnector import DbConnector


class DataProvider:
    def __init__(self):
        self.dataSets = {}
        self.db = DbConnector()

    def addOptions(self, ticker) -> None:
        self.dataSets[ticker + "_options"] = self.db.get_options(ticker)

    def useDataSet(self, name, dataset) -> None:
        self.db.getSet

        dataset["Date"] = pd.to_datetime(dataset["Date"])
        dataset.set_index("Date", inplace=True)
        self.dataSets[name] = dataset

    def _getSet(self, ticker):
        return self.db.getSet(ticker)

    def plotSet(self, name):
        df = self._getSet(name)
        df[["Open", "High", "Low", "Close"]].plot()
        plt.show()


if __name__ == '__main__':
    DataProvider().plotSet("aapl_daily")
