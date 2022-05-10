import datetime
from Portfolio import Portfolio
from ExecutionEngine import ExecutionEngine


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
