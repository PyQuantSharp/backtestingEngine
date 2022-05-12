def tickerIsOption(ticker: str) -> bool:
    if "aapl" in ticker:
        return False
    return True