import re
from dataclasses import dataclass
from typing import Optional

SYMBOL_RE = re.compile(r"^[A-Za-z0-9]{2,15}$")

@dataclass
class ParseResult:
    symbol: Optional[str] = None
    quote: Optional[str] = None
    exchange: Optional[str] = None
    dex: Optional[str] = None
    chain: Optional[str] = None
    address: Optional[str] = None
    approx_price: Optional[float] = None

def parse(text: str) -> ParseResult:
    t = text.strip().replace("\n", " ")
    res = ParseResult()

    m = re.search(r"addr:([0-9A-Za-zx]+)", t)
    if m:
        res.address = m.group(1)

    m = re.search(r"chain:([A-Za-z0-9]+)", t)
    if m:
        res.chain = m.group(1).upper()

    m = re.search(r"dex:([A-Za-z0-9_-]+)", t)
    if m:
        res.dex = m.group(1).lower()

    m = re.search(r"@([A-Za-z0-9_-]+)", t)
    if m and not t.__contains__("@~"):
        res.exchange = m.group(1).upper()

    m = re.search(r"pair:([A-Za-z0-9]+)", t)
    if m:
        res.quote = m.group(1).upper()

    m = re.search(r"@~([0-9]*\.?[0-9]+)", t)
    if m:
        res.approx_price = float(m.group(1))

    if res.address is None:
        token = t.split()[0]
        if "/" in token:
            sym, quo = token.split("/", 1)
            res.symbol = sym.upper()
            res.quote = (res.quote or quo.upper())
        else:
            if SYMBOL_RE.match(token):
                res.symbol = token.upper()
    return res
