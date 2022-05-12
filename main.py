import string
import datetime
import tkinter as tk
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from Utils import calculateProfitFactor
from enums import Timeframe
from DataProvider import DataProvider
from Broker import Broker
from TimeMachine import TimeMachine
from StrategyBase import StrategyBase


class Backtest:
    def __init__(self, strategy: StrategyBase, timerange: tuple[datetime.datetime, datetime.datetime],
                 timeframe: Timeframe, start_balance: float = 100000.0):
        self.strategy = strategy
        self.timerange = timerange
        self.timeframe = timeframe
        self.start_balance = start_balance
        self.dataProvider = DataProvider()
        self.timeMachine = TimeMachine(timerange, timeframe, self.dataProvider)
        self.broker = Broker(self.start_balance, self.timerange[0], self.dataProvider)

    def run(self) -> None:
        while True:
            snapshot = self.timeMachine.nextMoment()
            if snapshot["time"] >= self.timerange[1]:
                break
            new_data = False
            for dataset in snapshot["data"].values():
                if not dataset.empty:
                    new_data = True
                    break
            if not new_data:
                continue
            self.broker.executionEngine.checkOrders(snapshot)
            self.strategy.onData(snapshot, self.broker)
            self.broker.portfolio.updatePortfolio(snapshot)

        self.results()

    def results(self) -> None:
        ResultsWindow(self.broker.portfolio.history).mainloop()


class ResultsWindow(tk.Tk):
    def __init__(self, portfolio_history):
        self.portfolioHistory = portfolio_history
        super().__init__()

        self.title('Portfolio History')

        fig = Figure(dpi=100)
        plot1 = fig.add_subplot(111)
        print(self.portfolioHistory)
        self.portfolioHistory["Equity"] = self.portfolioHistory["balance"] + self.portfolioHistory["holdingsValue"]
        plot1.plot(self.portfolioHistory, markevery=10)
        plot1.legend(["Balance", "Holdings", "Equity"])
        print(calculateProfitFactor(self.portfolioHistory))
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack()
