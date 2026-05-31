"""Modelo de producto compartido por los scrapers."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    brand: Optional[str] = None
    size_ml: Optional[int] = None
    price_ars: float
    list_price: Optional[float] = None  # precio de lista (para calcular descuento)
    url: str
    store: Optional[str] = None
    ts: datetime
