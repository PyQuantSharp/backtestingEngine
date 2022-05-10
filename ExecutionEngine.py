class ExecutionEngine:
    def __init__(self):
        self.openOrders = []

    def executeOrder(
            self, order: dict,
            broker,
            order_executed_callback: callable,
            order_rejected_callback: callable
    ) -> None:
        if broker.portfolio.balance >= order["price"] * order["quantity"]:
            order["order_executed_callback"] = order_executed_callback
            self.openOrders.append(order)
        else:
            order_rejected_callback(order, "Not enough funds")

    def checkOrders(self, current_moment) -> None:
        for order in self.openOrders:
            order["order_executed_callback"](order, current_moment)
            self.openOrders.remove(order)
