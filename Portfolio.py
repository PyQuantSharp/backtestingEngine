import pandas as pd
from Utils import *


class Portfolio:
    def __init__(self, start_balance: float, start_date):
        self.balance = start_balance
        self.history = pd.DataFrame(columns=["balance"])
        self.history = pd.concat(
            [self.history, pd.DataFrame({"balance": self.balance, "holdingsValue": 0}, index=[start_date])])
        self.holdings = {}
        self.holdingsValue = 0.0
        self.x = False

    def updatePortfolio(self, current_moment) -> None:
        self._updateHoldingsValue(current_moment)
        self._saveToHistory(current_moment)
        pass

    def addTransaction(self, transaction: dict, current_moment) -> None:
        if self.x and 0:
            return
        else:
            print("HÄ")
        self.x = True
        print(transaction, current_moment["time"])
        self._updateBalance(transaction)
        self._updateHoldings(transaction)
        self._updateHoldingsValue(current_moment)
        self._saveToHistory(current_moment)

    def _updateBalance(self, transaction: dict) -> None:
        self.balance -= transaction["quantity"] * transaction["price"]

    def _updateHoldings(self, transaction: dict) -> None:
        if not transaction["ticker"] in self.holdings:
            self.holdings[transaction["ticker"]] = {"quantity": transaction["quantity"],
                                                    "value": transaction["quantity"] * transaction["price"]}
        else:
            self.holdings[transaction["ticker"]]["quantity"] += transaction["quantity"]
            self.holdings[transaction["ticker"]]["value"] += transaction["quantity"] * transaction["price"]

    def _saveToHistory(self, current_moment) -> None:
        self.history = pd.concat([self.history, pd.DataFrame({
            "balance": self.balance,
            "holdingsValue": self.holdingsValue,
        }, index=[current_moment["time"]])])

    def _updateHoldingsValue(self, current_moment: dict) -> None:
        self.holdingsValue = 0.0
        expired_options = []
        for ticker, holding in self.holdings.items():
            if tickerIsOption(ticker):
                underlying = current_moment["data"][getUnderlying(ticker)]
                underlying = underlying[underlying["time"] <= current_moment["time"]]

                if current_moment["time"] > getExpirationDate(ticker):
                    # self.holdingsValue += underlying.iloc[-1]["close"] * holding["quantity"]
                    self.balance += holding["quantity"] * (underlying.iloc[-1]["close"] - getStrikePrice(ticker))
                    expired_options.append(ticker)
                else:
                    self.holdingsValue += (underlying.iloc[-1]["close"] - getStrikePrice(ticker)) * holding["quantity"]
            else:
                self.holdingsValue += current_moment["data"][ticker].iloc[-1]["close"] * holding["quantity"]
        for ticker in expired_options:
            del self.holdings[ticker]
