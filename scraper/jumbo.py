from __future__ import annotations

from datetime import datetime
import re
from typing import Optional

import requests
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    brand: Optional[str] = None
    size_ml: Optional[int] = None
    price_ars: float
    url: str
    ts: datetime


PRODUCT_RE = re.compile(
    r'<article class="product"\s+data-name="(?P<name>[^"]+)"\s+'
    r'data-brand="(?P<brand>[^"]*)"\s+'
    r'data-size="(?P<size>\d+)"\s+'
    r'data-price="(?P<price>[\d,.]+)"[^>]*>\s*'
    r'<a href="(?P<url>[^"]+)"',
    re.S,
)


def _parse(html: str) -> list[Product]:
    items: list[Product] = []
    for m in PRODUCT_RE.finditer(html):
        price = float(m.group('price').replace(',', '.'))
        size = int(m.group('size')) if m.group('size') else None
        items.append(
            Product(
                name=m.group('name'),
                brand=m.group('brand') or None,
                size_ml=size,
                price_ars=price,
                url=m.group('url'),
                ts=datetime.utcnow(),
            )
        )
    return items


def scrape(html: str | None = None) -> list[Product]:
    if html is None:
        resp = requests.get('https://jumbo.example.com')
        html = resp.text
    return _parse(html)
