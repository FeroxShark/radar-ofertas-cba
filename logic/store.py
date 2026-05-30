"""Almacenamiento local de precios scrapeados (JSON, sin servicios externos)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from scraper.base import Product


def load_prices(path: Path) -> list[dict]:
    """Lee el historial de precios; devuelve lista vacía si no existe."""
    if not path.exists():
        return []
    return json.loads(path.read_text())


def append_prices(products: Iterable[Product], path: Path) -> int:
    """Agrega productos al historial local. Devuelve cuántos se guardaron."""
    products = list(products)
    history = load_prices(path)
    history.extend(p.model_dump(mode="json") for p in products)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, ensure_ascii=False, indent=2))
    return len(products)
