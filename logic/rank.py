"""Ranking de ofertas a partir del historial local de precios."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta

from pydantic import BaseModel

import config


class Deal(BaseModel):
    name: str
    brand: str | None = None
    size_ml: int | None = None
    price_ars: float
    price_unit: float
    url: str
    store: str | None = None
    ts: datetime
    savings_pct: float


def _as_dt(value) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def generate_deals(
    records: list[dict],
    top_n: int | None = None,
    window_days: int | None = None,
) -> list[Deal]:
    """Calcula el ahorro de cada producto vs su promedio histórico.

    `records` es una lista de dicts de precios (name, price_ars, size_ml, url,
    store, ts). Devuelve las mejores `top_n` ofertas ordenadas por ahorro.
    """
    top_n = top_n if top_n is not None else config.TOP_N
    window_days = window_days if window_days is not None else config.PRICE_WINDOW_DAYS
    since = datetime.utcnow() - timedelta(days=window_days)

    items = []
    for r in records:
        if _as_dt(r["ts"]) < since:
            continue
        size = r.get("size_ml") or 1
        items.append({**r, "price_unit": r["price_ars"] / size})

    history = defaultdict(list)
    for it in items:
        history[it["name"]].append(it["price_unit"])
    averages = {k: sum(v) / len(v) for k, v in history.items()}

    deals: list[Deal] = []
    for it in items:
        mean = averages[it["name"]]
        savings = (mean - it["price_unit"]) / mean * 100 if mean else 0.0
        deals.append(
            Deal(
                name=it["name"],
                brand=it.get("brand"),
                size_ml=it.get("size_ml"),
                price_ars=it["price_ars"],
                price_unit=it["price_unit"],
                url=it["url"],
                store=it.get("store"),
                ts=_as_dt(it["ts"]),
                savings_pct=savings,
            )
        )

    deals.sort(key=lambda d: d.savings_pct, reverse=True)
    return deals[:top_n]
