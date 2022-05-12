import string

from Broker import Broker


class StrategyBase:
    def __init__(self, strategy_name: string):
        self.strategy_name = strategy_name

    def onData(self, snapshot, broker: Broker) -> None:
        raise NotImplementedError("onData not defined in strategy")
