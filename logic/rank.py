"""Ranking de ofertas a partir del descuento real (precio vs precio de lista)."""
from __future__ import annotations

from datetime import datetime, timedelta

from pydantic import BaseModel

import config


class Deal(BaseModel):
    name: str
    brand: str | None = None
    size_ml: int | None = None
    price_ars: float
    list_price: float | None = None
    price_unit: float | None = None
    url: str
    store: str | None = None
    ts: datetime
    savings_pct: float


def _as_dt(value) -> datetime:
    if isinstance(value, datetime):
        return value
    return datetime.fromisoformat(str(value))


def _savings(price: float, list_price: float | None) -> float:
    """% de descuento del precio actual respecto del precio de lista."""
    if list_price and list_price > price:
        return (list_price - price) / list_price * 100
    return 0.0


def generate_deals(
    records: list[dict],
    top_n: int | None = None,
    window_days: int | None = None,
    min_savings: float = 0.0,
) -> list[Deal]:
    """Devuelve las mejores ofertas reales (precio < precio de lista).

    `records` es una lista de dicts de productos (name, price_ars, list_price,
    size_ml, url, store, ts). Solo se incluyen productos con descuento mayor a
    `min_savings`, ordenados por mayor descuento.
    """
    top_n = top_n if top_n is not None else config.TOP_N
    window_days = window_days if window_days is not None else config.PRICE_WINDOW_DAYS
    since = datetime.utcnow() - timedelta(days=window_days)

    deals: list[Deal] = []
    for r in records:
        if _as_dt(r["ts"]) < since:
            continue
        savings = _savings(r["price_ars"], r.get("list_price"))
        if savings <= min_savings:
            continue
        size = r.get("size_ml")
        deals.append(
            Deal(
                name=r["name"],
                brand=r.get("brand"),
                size_ml=size,
                price_ars=r["price_ars"],
                list_price=r.get("list_price"),
                price_unit=(r["price_ars"] / size) if size else None,
                url=r["url"],
                store=r.get("store"),
                ts=_as_dt(r["ts"]),
                savings_pct=savings,
            )
        )

    deals.sort(key=lambda d: d.savings_pct, reverse=True)
    return deals[:top_n]
