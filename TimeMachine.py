import datetime
from enums import Timeframe
from DataProvider import DataProvider


class TimeMachine:
    def __init__(self, timerange: tuple[datetime.datetime, datetime.datetime], timeframe: Timeframe,
                 data_provider: DataProvider):
        self.timerange = timerange
        self.dataProvider = data_provider
        self.timeframe = timeframe
        self._currentMoment = timerange[0]

    def nextMoment(self):
        match self.timeframe:
            case Timeframe.DAILY:
                snapshot = self.nextDay()
                self._currentMoment = self._currentMoment + datetime.timedelta(days=1)
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

    def nextDay(self):
        for name, dataset in self.dataProvider.dataSets.items():
            try:
                return {"data": dataset.loc[:self._currentMoment:], "time": self._currentMoment}
            except KeyError as e:
                print("No data in Dataset", name, "for", self._currentMoment)
