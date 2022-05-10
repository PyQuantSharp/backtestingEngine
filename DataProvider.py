import pandas as pd
from DbConnector import DbConnector

class DataProvider:
    def __init__(self):
        self.dataSets = {
            "options": {}
        }
        self.db = DbConnector().connect()

    def addOptions(self, ticker) -> None:
        self.dataSets["options"]["ticker"] = self._getSet("options", ticker)

    def addDataSet(self, name, dataset) -> None:
        dataset["Date"] = pd.to_datetime(dataset["Date"])
        dataset.set_index("Date", inplace=True)
        self.dataSets[name] = dataset

    def _getSet(self, type, ticker) -> pd.DataFrame:
        match type:
            case "options":
                pass
