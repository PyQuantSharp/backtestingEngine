import datetime
from typing import Any


def tickerIsOption(ticker: str) -> bool:
    if "aapl" in ticker:
        return False
    return True


def getUnderlying(ticker: str) -> str:
    return "SPY"


def getStrikePrice(ticker: str) -> float:
    return 250.0


def calculateProfitFactor(x: Any) -> float:
    return 1.1


def getExpirationDate(ticker: str) -> datetime.datetime:
    return datetime.datetime(2020, 12, 18, 0, 0, 0)
