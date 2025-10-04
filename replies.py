from textwrap import dedent

def make_reply(symbol, market, ctx, sig, stats):
    return dedent(f"""
    *{symbol}* — {market}
    24h: *{stats['pct24h']:+.2f}%* | Vol: *{stats['vol24h']}*
    Trend: *{ctx['trend']}* | RSI(1h): *{ctx['rsi1h']:.0f}* | MACD(1h): *{ctx['macd_state']}*

    *Setup*: {sig.verdict}
    *Entry*: {sig.entry_zone}
    *SL*: `{sig.sl_level}`
    *TP1/TP2/TP3*: `{sig.tp1}` / `{sig.tp2}` / `{sig.tp3}`
    *Riska birka*: {sig.risk} | *Score*: {sig.score}/100

    _Ne finanšu padoms._
    """)
