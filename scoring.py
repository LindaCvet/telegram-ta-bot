def macd_state(macd, signal):
    if macd > signal: return "bullish"
    if macd < signal: return "bearish"
    return "flat"

def score(trend_up: bool, macd_bull: bool, rsi: float, anti_fomo: bool) -> int:
    s = 50
    if trend_up: s += 15
    if macd_bull: s += 10
    if 55 <= rsi <= 70: s += 10
    if anti_fomo: s -= 5
    return max(0, min(s, 100))
