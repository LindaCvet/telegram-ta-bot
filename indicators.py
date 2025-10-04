import pandas as pd
import pandas_ta as ta

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.set_index("ts", inplace=True)
    out["rsi14"] = ta.rsi(out["close"], length=14)
    macd = ta.macd(out["close"], fast=12, slow=26, signal=9)
    out["macd"] = macd["MACD_12_26_9"]
    out["macd_signal"] = macd["MACDs_12_26_9"]
    out["macd_hist"] = macd["MACDh_12_26_9"]
    out["atr14"] = ta.atr(out["high"], out["low"], out["close"], length=14)
    out["ema20"] = ta.ema(out["close"], length=20)
    out["ema50"] = ta.ema(out["close"], length=50)
    out["ema200"] = ta.ema(out["close"], length=200)
    out.reset_index(inplace=True)
    return out
