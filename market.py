import ccxt
import pandas as pd
from typing import Optional

SUPPORTED = {
    "BINANCE": ccxt.binance,
    "COINBASE": ccxt.coinbase,
}

def make_exchange(name: Optional[str]):
    name = (name or "BINANCE").upper()
    if name not in SUPPORTED:
        raise ValueError(f"Neatbalstīta birža: {name}")
    ex = SUPPORTED[name]()
    ex.load_markets()
    return ex

def pick_symbol(ex, base: str, quote: Optional[str]) -> str:
    quote = (quote or "USDT").upper()
    sym = f"{base}/{quote}"
    if sym in ex.symbols:
        return sym
    if f"{base}/USD" in ex.symbols:
        return f"{base}/USD"
    raise ValueError("Pāris nav atrodams (simbols/quote)")

def fetch_ohlcv(ex, symbol: str, timeframe: str = "1h", limit: int = 500) -> pd.DataFrame:
    ohlcv = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=["ts","open","high","low","close","volume"])
    df["ts"] = pd.to_datetime(df["ts"], unit="ms")
    return df

def fetch_ticker24h(ex, symbol: str) -> dict:
    return ex.fetch_ticker(symbol)
