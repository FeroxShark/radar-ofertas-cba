"""Lógica común de scraping compartida por todos los retailers."""
from __future__ import annotations

from datetime import datetime
from typing import Callable, Optional, Pattern

import requests
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    brand: Optional[str] = None
    size_ml: Optional[int] = None
    price_ars: float
    url: str
    store: Optional[str] = None
    ts: datetime


def parse(html: str, pattern: Pattern[str], store: str | None = None) -> list[Product]:
    """Extrae productos de `html` usando el `pattern` del retailer."""
    products: list[Product] = []
    for m in pattern.finditer(html):
        price = float(m.group("price").replace(",", "."))
        size = int(m.group("size")) if m.group("size") else None
        products.append(
            Product(
                name=m.group("name"),
                brand=m.group("brand") or None,
                size_ml=size,
                price_ars=price,
                url=m.group("url"),
                store=store,
                ts=datetime.utcnow(),
            )
        )
    return products


def build_scraper(
    url: str, pattern: Pattern[str], store: str | None = None
) -> Callable[[Optional[str]], list[Product]]:
    """Devuelve una función `scrape(html=None)` para un retailer concreto."""

    def scrape(html: str | None = None) -> list[Product]:
        if html is None:
            html = requests.get(url).text
        return parse(html, pattern, store)

    return scrape
