import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
DEFAULT_QUOTE = "USDT"
ANTI_FOMO_PCT = 15.0  # 24h %
DEFAULT_RISK = "vidējs"  # zems | vidējs | augsts
