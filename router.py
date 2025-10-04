from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot import parser
from data.market import make_exchange, pick_symbol, fetch_ohlcv, fetch_ticker24h
from ta.indicators import add_indicators
from bot.scoring import macd_state, score
from bot.replies import make_reply
from bot.risk import anti_fomo

router = Router()

@router.message(Command("start"))
async def start(m: Message):
    await m.answer(
        "Sveiki! Sūti man monētu: `addr:0x... chain:ETH` vai `SYMBOL/USDT@BINANCE` vai vienkārši `BTC`.\n"
        "Es atdošu: vai vērts pirkt, Entry/SL/TP, trendu un risku.",
        parse_mode="Markdown"
    )

@router.message(F.text)
async def handle_symbol(m: Message):
    q = m.text.strip()
    p = parser.parse(q)

    if not (p.address or p.symbol):
        await m.answer("Nepietiek info. Piem.: `CATI/USDT@BINANCE` vai `addr:0x.. chain:ETH`", parse_mode="Markdown")
        return

    try:
        ex = make_exchange(p.exchange)
        symbol = pick_symbol(ex, (p.symbol or "BTC"), p.quote)
    except Exception as e:
        await m.answer(f"Neizdevās atrast pāri: {e}")
        return

    try:
        df1h = add_indicators(fetch_ohlcv(ex, symbol, timeframe="1h", limit=400))
        df4h = add_indicators(fetch_ohlcv(ex, symbol, timeframe="4h", limit=400))
        df1d = add_indicators(fetch_ohlcv(ex, symbol, timeframe="1d", limit=400))
        df15 = add_indicators(fetch_ohlcv(ex, symbol, timeframe="15m", limit=400))
    except Exception as e:
        await m.answer(f"Datu kļūda (OHLCV): {e}")
        return

    try:
        t = fetch_ticker24h(ex, symbol)
        last = float(t.get("last", t.get("close", 0)))
        open_ = float(t.get("open", last))
        pct24h = (last - open_) / open_ * 100 if open_ else 0.0
        vol24h = t.get("baseVolume") or t.get("quoteVolume") or "—"
    except Exception:
        pct24h, vol24h = 0.0, "—"

    c1, c4, cd = df1h.iloc[-1], df4h.iloc[-1], df1d.iloc[-1]
    trend_up = (c1.close > c1.ema50) and (c4.close > c4.ema50) and (cd.close > cd.ema50)

    macd_state_1h = macd_state(c1.macd, c1.macd_signal)
    s = score(trend_up, macd_state_1h == "bullish", float(c1.rsi14 or 50), anti_fomo(pct24h))

    c15 = df15.iloc[-1]
    atr = float(c15.atr14 or 0)
    price = float(c15.close)
    sl = price - 1.5 * atr
    tp1, tp2, tp3 = price + 1.0*atr, price + 2.0*atr, price + 3.0*atr

    setup = "Buy pullback" if anti_fomo(pct24h) else "Speculative breakout"
    entry_zone = "Pullback uz 20 EMA / virs mini-range" if anti_fomo(pct24h) else "Breakout virs pēdējā 15m high"

    text = make_reply(
        symbol,
        market=p.exchange or "BINANCE",
        ctx={
            "trend": "↑" if trend_up else "↓",
            "rsi1h": float(c1.rsi14 or 50),
            "macd_state": macd_state_1h,
        },
        sig=type("S", (), {
            "verdict": setup,
            "risk": "vidējs",
            "entry_zone": entry_zone,
            "sl_level": round(sl, 6),
            "tp1": round(tp1, 6),
            "tp2": round(tp2, 6),
            "tp3": round(tp3, 6),
            "score": s,
        })(),
        stats={"pct24h": pct24h, "vol24h": vol24h}
    )

    await m.answer(text, parse_mode="Markdown")
