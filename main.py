import string
import datetime
from enum import Enum

import pandas as pd


class StrategyBase:
    def __init__(self, strategy_name: string):
        self.strategy_name = strategy_name

    def onData(self, data: pd.DataFrame) -> None:
        raise NotImplementedError("onData not defined in strategy")


class DataProvider:
    def __init__(self):
        self.dataSets = {}

    def addDataSet(self, name: string, dataset: pd.DataFrame) -> None:
        dataset["Date"] = pd.to_datetime(dataset["Date"])
        dataset.set_index("Date", inplace=True)

        self.dataSets[name] = dataset


class Timeframe(Enum):
    DAILY = "daily"
    MINUTE = "minute"
    SECOND = "second"
    TICK = "tick"


class TimeMachine:
    def __init__(self, timerange: tuple[datetime.datetime, datetime.datetime], timeframe: Timeframe,
                 data_provider: DataProvider):
        self.timerange = timerange
        self.dataProvider = data_provider
        self.timeframe = timeframe
        self.currentMoment = timerange[0]

    def nextMoment(self) -> pd.DataFrame:
        match self.timeframe:
            case Timeframe.DAILY:
                moment = self.nextDay()
                self.currentMoment = self.currentMoment + datetime.timedelta(days=1)
                return moment
                pass
            case Timeframe.MINUTE:
                pass
            case Timeframe.SECOND:
                pass
            case Timeframe.TICK:
                pass
            case _:
                raise ValueError("Unknown timeframe")

    def nextDay(self) -> pd.DataFrame:
        for name, dataset in self.dataProvider.dataSets.items():
            try:
                return dataset.loc[:self.currentMoment:]
            except KeyError as e:
                print("No data in Dataset", name, "for", self.currentMoment)


class Backtest:
    def __init__(self, strategy: StrategyBase, timerange: tuple[datetime.datetime, datetime.datetime],
                 timeframe: Timeframe, start_balance: float = 100000.0):
        self.strategy = strategy
        self.timerange = timerange
        self.timeframe = timeframe
        self.start_balance = start_balance
        self.broker = Broker(self.start_balance)
        self.dataProvider = DataProvider()
        self.timeMachine = TimeMachine(timerange, timeframe, self.dataProvider)

    def run(self) -> None:
        while self.timeMachine.currentMoment < self.timerange[1]:
            snapshot = self.timeMachine.nextMoment()
            self.strategy.onData(snapshot, self.broker)

    def results(self) -> None:
        pass


class Broker:
    def __init__(self, start_balance: float):
        self.balance = start_balance

    pass


class Portfolio:
    def __init__(self, broker: Broker, start_balance: float):
        self.broker = broker
        self.holdings = {}
        self.balance = start_balance


class ExecutionEngine:
    pass
