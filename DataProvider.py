import datetime

import pandas as pd
from DbConnector import DbConnector


class DataProvider:
    def __init__(self):
        self.dataSets = {}
        self.db = DbConnector()

    def addDataset(self, dataset: dict) -> None:
        match dataset["source"]:
            case "Database":
                df = self._getDatasetFromDb(dataset)
            case "File":
                df = self._getDatasetFromFile(dataset)
                pass
            case "DataFrame":
                df = dataset["set"]
                pass
            case _:
                raise Exception("Unknown source")

        df["time"] = pd.to_datetime(df["time"])
        df.index = pd.to_datetime(df["time"])
        self.dataSets[dataset["name"]] = df

    def getTickers(self, timestamp: datetime.datetime) -> list:
        tickers = []
        for key in self.dataSets.keys():
            if "symbol" in self.dataSets[key].columns:
                for i in self.dataSets[key][self.dataSets[key].index <= timestamp]["symbol"].unique():
                    tickers.append(i)
            else:
                tickers.append(key)
        return tickers

    def _getDatasetFromDb(self, dataset: dict) -> pd.DataFrame:
        df = self.db.getTable(dataset["set"])
        return df

    def _getDatasetFromFile(self, dataset: dict) -> pd.DataFrame:
        return pd.read_csv(dataset["set"])


if __name__ == '__main__':
    DataProvider().addDataset({
        "name": "spy_options_eod1",
        "source": "Database",
        "set": "spy_options_eod",
    })

    DataProvider().addDataset({
        "name": "spy_options_eod2",
        "source": "DataFrame",
        "set": pd.read_csv("exampleData/spy_options_eod.csv"),
    })

    DataProvider().addDataset({
        "name": "spy_options_eod3",
        "source": "File",
        "set": "exampleData/spy_options_eod.csv",
    })
