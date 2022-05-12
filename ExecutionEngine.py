class ExecutionEngine:
    def __init__(self):
        self.openOrders = []

    def executeOrder(
            self, order: dict,
            broker,
            current_moment,
            order_executed_callback: callable,
            order_rejected_callback: callable
    ) -> None:
        if broker.portfolio.balance >= current_moment["data"][order["ticker"]].iloc[-1]["close"] * order["quantity"]:
            order["order_executed_callback"] = order_executed_callback
            order["price"] = current_moment["data"][order["ticker"]].iloc[-1]["close"]
            self.openOrders.append(order)
        else:
            order_rejected_callback(order, "Not enough funds")

    def checkOrders(self, current_moment) -> None:
        for order in self.openOrders:
            order["order_executed_callback"](order, current_moment)
            self.openOrders.remove(order)
