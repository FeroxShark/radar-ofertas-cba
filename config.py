"""Configuración central del proyecto.

Lee todo desde variables de entorno (con `.env` opcional vía python-dotenv).
Sin servicios externos: los precios se guardan en un JSON local y la salida es
una página web estática.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent


def _int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except (TypeError, ValueError):
        return default


# Almacenamiento local de precios scrapeados
DATA_DIR = Path(os.environ.get("DATA_DIR", ROOT / "data"))
PRICES_FILE = DATA_DIR / "prices.json"

# Salida web
WEB_DIR = Path(os.environ.get("WEB_DIR", ROOT / "web"))

# Ranking
PRICE_WINDOW_DAYS = _int("PRICE_WINDOW_DAYS", 30)
TOP_N = _int("TOP_N", 20)
