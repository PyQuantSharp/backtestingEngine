import string


class OptionContract:
    def __init__(self, ticker: string):
        self.ticker = ticker
        self.strike = 200
