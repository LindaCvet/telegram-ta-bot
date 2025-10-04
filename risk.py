from config import ANTI_FOMO_PCT

def anti_fomo(pct24h: float) -> bool:
    return pct24h >= ANTI_FOMO_PCT

def risk_label(level: str) -> str:
    return level
