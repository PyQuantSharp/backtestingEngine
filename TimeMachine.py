import datetime
from typing import Any

import pandas as pd

from enums import Timeframe
from DataProvider import DataProvider


class TimeMachine:
    def __init__(self, timerange: tuple[datetime.datetime, datetime.datetime], timeframe: Timeframe,
                 data_provider: DataProvider):
        self.timeframe = timeframe
        self.timerange = timerange
        if timeframe == Timeframe.DAILY:
            self.timerange = (timerange[0].date(), timerange[1].date())
        self.dataProvider = data_provider
        self._currentTime = timerange[0]

    def nextMoment(self):
        match self.timeframe:
            case Timeframe.DAILY:
                snapshot = self.nextDay()
                self._currentTime = self._currentTime + datetime.timedelta(days=1)
                return snapshot
                pass
            case Timeframe.MINUTE:
                raise NotImplementedError
                pass
            case Timeframe.SECOND:
                raise NotImplementedError
                pass
            case Timeframe.TICK:
                raise NotImplementedError
                pass
            case _:
                raise ValueError("Unknown timeframe")

    def nextDay(self) -> dict[str, Any]:
        snapshot = {
            "time": self._currentTime,
            "data": {}
        }
        for name, dataset in self.dataProvider.dataSets.items():
            if self._currentTime in dataset.index:
                snapshot["data"][name] = dataset.loc[:self._currentTime:]
            else:
                snapshot["data"][name] = pd.DataFrame()
        return snapshot