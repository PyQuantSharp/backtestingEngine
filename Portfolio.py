import datetime
import pandas as pd

class Portfolio:
    def __init__(self, start_balance: float, start_date: datetime.datetime):
        self.balance = start_balance
        self.history = pd.DataFrame(columns=["balance"])
        self.history = pd.concat(
            [self.history, pd.DataFrame({"balance": self.balance, "holdingsValue": 0}, index=[start_date])])
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
        self.balance -= transaction["quantity"] * transaction["price"]

    def _updateHoldings(self, transaction: dict) -> None:
        if not transaction["symbol"] in self.holdings:
            self.holdings[transaction["symbol"]] = {"quantity": transaction["quantity"],
                                                    "value": transaction["quantity"] * transaction["price"]}
        else:
            self.holdings[transaction["symbol"]]["quantity"] += transaction["quantity"]
            self.holdings[transaction["symbol"]]["value"] += transaction["quantity"] * transaction["price"]

    def _saveToHistory(self, current_moment: datetime.datetime) -> None:
        self.history = pd.concat([self.history, pd.DataFrame({
            "balance": self.balance,
            "holdingsValue": self.holdingsValue,
        }, index=[current_moment["time"]])])

    def _updateHoldingsValue(self, current_moment) -> None:
        self.holdingsValue = 0.0
        for symbol, holding in self.holdings.items():
            self.holdingsValue += current_moment["data"].iloc[-1]["Close"] * holding["quantity"]
