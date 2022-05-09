import string
import datetime
from enum import Enum
import tkinter as tk

import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Timeframe(Enum):
    DAILY = "daily"
    MINUTE = "minute"
    SECOND = "second"
    TICK = "tick"


class DataProvider:
    def __init__(self):
        self.dataSets = {}

    def addDataSet(self, name: string, dataset: pd.DataFrame) -> None:
        dataset["Date"] = pd.to_datetime(dataset["Date"])
        dataset.set_index("Date", inplace=True)

        self.dataSets[name] = dataset


class ExecutionEngine:
    def __init__(self):
        self.openOrders = []

    def executeOrder(
            self, order: dict,
            broker,
            order_executed_callback: callable,
            order_rejected_callback: callable
    ) -> None:
        if order["action"] == "buy":
            if broker.portfolio.balance >= order["price"] * order["quantity"]:
                order["order_executed_callback"] = order_executed_callback
                self.openOrders.append(order)
            else:
                order_rejected_callback(order, "Not enough funds")

    def checkOrders(self, current_moment) -> None:
        for order in self.openOrders:
            order["order_executed_callback"](order, current_moment)
            self.openOrders.remove(order)


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


class Broker:
    def __init__(self, start_balance: float, start_date: datetime.datetime):
        self.openOrders = []
        self.portfolio = Portfolio(start_balance, start_date)
        self.executionEngine = ExecutionEngine()

    def addOrder(self, order: dict):
        self.openOrders.append(order)
        self.executionEngine.executeOrder(
            order,
            self,
            order_executed_callback=self._onOrderExecuted,
            order_rejected_callback=self._onOrderRejected
        )

    def _onOrderRejected(self, order: dict, reason: str):
        print("Order rejected:", order, reason)

    def _onOrderExecuted(self, transaction: dict, current_moment: datetime.datetime):
        self.portfolio.addTransaction(transaction, current_moment)
        self.openOrders.remove(transaction)


class StrategyBase:
    def __init__(self, strategy_name: string):
        self.strategy_name = strategy_name

    def onData(self, snapshot, broker: Broker) -> None:
        raise NotImplementedError("onData not defined in strategy")


class Backtest:
    def __init__(self, strategy: StrategyBase, timerange: tuple[datetime.datetime, datetime.datetime],
                 timeframe: Timeframe, start_balance: float = 100000.0):
        self.strategy = strategy
        self.timerange = timerange
        self.timeframe = timeframe
        self.start_balance = start_balance
        self.dataProvider = DataProvider()
        self.timeMachine = TimeMachine(timerange, timeframe, self.dataProvider)
        self.broker = Broker(self.start_balance, self.timerange[0])

    def run(self) -> None:
        while True:
            snapshot = self.timeMachine.nextMoment()
            if snapshot["time"] >= self.timerange[1]:
                break
            self.broker.executionEngine.checkOrders(snapshot)
            self.strategy.onData(snapshot, self.broker)
            self.broker.portfolio.updatePortfolio(snapshot)
        self.results()

    def results(self) -> None:
        reswin = ResultsWindow(self.broker.portfolio.history)
        reswin.mainloop()


class Portfolio:
    def __init__(self, start_balance: float, start_date: datetime.datetime):
        self.balance = start_balance
        self.history = pd.DataFrame(columns=["balance"])
        self.history = pd.concat([self.history, pd.DataFrame({"balance": self.balance, "holdingsValue": 0}, index=[start_date])])
        self.holdings = {}
        self.holdingsValue = 0.0

    def updatePortfolio(self, current_moment) -> None:
        self._updateHoldingsValue(current_moment)
        self._saveToHistory(current_moment)
        pass

    def addTransaction(self, transaction: dict, current_moment: datetime.datetime) -> None:
        self._updateBalance(transaction)
        self._updateHoldings(transaction)
        self._updateHoldingsValue(current_moment)
        self._saveToHistory(current_moment)

    def _updateBalance(self, transaction: dict) -> None:
        if transaction["action"] == "buy":
            self.balance -= transaction["quantity"] * transaction["price"]
        elif transaction["action"] == "sell":
            self.balance += transaction["quantity"] * transaction["price"]

    def _updateHoldings(self, transaction: dict) -> None:
        if transaction["action"] == "buy":
            if not transaction["symbol"] in self.holdings:
                self.holdings[transaction["symbol"]] = {"quantity": transaction["quantity"],
                                                        "value": transaction["quantity"] * transaction["price"]}
            else:
                self.holdings[transaction["symbol"]]["quantity"] += transaction["quantity"]
                self.holdings[transaction["symbol"]]["value"] += transaction["quantity"] * transaction["price"]
        elif transaction["action"] == "sell":
            if not transaction["symbol"] in self.holdings:
                self.holdings[transaction["symbol"]] = {"quantity": transaction["quantity"],
                                                        "value": transaction["quantity"] * transaction["price"]}
            else:
                self.holdings[transaction["symbol"]]["quantity"] -= transaction["quantity"]
                self.holdings[transaction["symbol"]]["value"] -= transaction["quantity"] * transaction["price"]

    def _saveToHistory(self, current_moment: datetime.datetime) -> None:
        self.history = pd.concat([self.history, pd.DataFrame({
            "balance": self.balance,
            "holdingsValue": self.holdingsValue,
        }, index=[current_moment["time"]])])

    def _updateHoldingsValue(self, current_moment) -> None:
        self.holdingsValue = 0.0
        for symbol, holding in self.holdings.items():
            self.holdingsValue += current_moment["data"].iloc[-1]["Close"] * holding["quantity"]


class ResultsWindow(tk.Tk):
    def __init__(self, portfolio_history):
        self.portfolioHistory = portfolio_history
        super().__init__()

        self.title('Portfolio History')

        fig = Figure(dpi=100)
        plot1 = fig.add_subplot(111)
        print(self.portfolioHistory)
        self.portfolioHistory["Equity"] = self.portfolioHistory["balance"] + self.portfolioHistory["holdingsValue"]
        plot1.plot(self.portfolioHistory)
        plot1.legend(["Balance", "Holdings", "Equity"])

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack()
