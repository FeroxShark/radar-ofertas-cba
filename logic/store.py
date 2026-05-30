"""Persistencia de productos scrapeados en Firestore."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

from scraper.base import Product


def save_products(db, products: Iterable[Product], retailer: str | None = None) -> int:
    """Guarda productos en la colección `prices` y registra el último `ts`.

    `db` es un cliente Firestore (inyectable para tests). Devuelve la cantidad
    de productos guardados. Actualiza `scraper_logs/<retailer>` con el momento
    del scrapeo, que es lo que consume `self_check`.
    """
    products = list(products)
    prices = db.collection("prices")
    for p in products:
        prices.add(p.model_dump())

    if retailer:
        db.collection("scraper_logs").document(retailer).set(
            {"ts": datetime.utcnow(), "count": len(products)}
        )
    return len(products)
