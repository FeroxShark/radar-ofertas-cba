"""Registro de scrapers de retailers."""
from __future__ import annotations

from .base import Product
from . import carrefour, dia, jumbo, mercadolibre

RETAILERS = {
    "carrefour": carrefour,
    "dia": dia,
    "jumbo": jumbo,
    "mercadolibre": mercadolibre,
}


def scrape_all() -> list[Product]:
    """Corre todos los scrapers registrados y junta los productos."""
    products: list[Product] = []
    for module in RETAILERS.values():
        products.extend(module.scrape())
    return products


__all__ = ["Product", "RETAILERS", "scrape_all"]
