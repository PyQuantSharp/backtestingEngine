from Utils import tickerIsOption


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
        # print("Executing order:", order, current_moment["time"])
        if tickerIsOption(order["ticker"]):
            df = current_moment["data"][order["dataset"]]
            df = df[df["symbol"] == order["ticker"]]
            if df.shape[0] == 0:
                order_rejected_callback(order, "No data for ticker")
                return
            df = df.iloc[-1]
            if broker.portfolio.balance >= order["quantity"] * df["close"]:
                order["order_executed_callback"] = order_executed_callback
                order["price"] = df["close"]
                self.openOrders.append(order)
                order["order_executed_callback"](order, current_moment)
                self.openOrders.remove(order)
        else:
            if broker.portfolio.balance >= current_moment["data"][order["ticker"]].iloc[-1]["close"] * order["quantity"]:
                order["order_executed_callback"] = order_executed_callback
                order["price"] = current_moment["data"][order["ticker"]].iloc[-1]["close"]
                self.openOrders.append(order)
                order["order_executed_callback"](order, current_moment)
                self.openOrders.remove(order)
            else:
                order_rejected_callback(order, "Not enough funds")

    def checkOrders(self, current_moment) -> None:
        for order in self.openOrders:
            order["order_executed_callback"](order, current_moment)
            self.openOrders.remove(order)
