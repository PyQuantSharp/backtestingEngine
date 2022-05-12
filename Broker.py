import datetime

from DataProvider import DataProvider
from Portfolio import Portfolio
from ExecutionEngine import ExecutionEngine


class Broker:
    def __init__(self, start_balance: float, start_date: datetime.datetime, data_provider: DataProvider) -> None:
        self.openOrders = []
        self.portfolio = Portfolio(start_balance, start_date)
        self.executionEngine = ExecutionEngine()
        self.dataProvider = data_provider
        self.x = False

    def addOrder(self, order: dict, current_moment) -> None:
        self.openOrders.append(order)
        self.executionEngine.executeOrder(
            order,
            self,
            current_moment,
            order_executed_callback=self._onOrderExecuted,
            order_rejected_callback=self._onOrderRejected
        )

    def getTickers(self, timestamp: datetime.datetime) -> list:
        return self.dataProvider.getTickers(timestamp)

    def _onOrderRejected(self, order: dict, reason: str):
        # print("Order rejected:", order, reason)
        pass

    def _onOrderExecuted(self, transaction: dict, current_moment):
        # print("Order executed:", transaction)
        self.portfolio.addTransaction(transaction, current_moment)
        self.openOrders.remove(transaction)
