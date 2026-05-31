"""Registro de tiendas y scrapeo agregado.

Las tiendas soportadas corren sobre VTEX, que expone una API pública de
catálogo. `scrape_all` busca una canasta de términos en cada tienda y junta
los productos disponibles.
"""
from __future__ import annotations

from .base import Product
from . import vtex

# Tiendas VTEX de Argentina (host base de cada una).
STORES = {
    "Carrefour": "https://www.carrefour.com.ar",
    "Día": "https://diaonline.supermercadosdia.com.ar",
}

# Canasta de términos a buscar en cada tienda.
DEFAULT_TERMS = [
    "leche",
    "aceite",
    "yerba",
    "cafe",
    "fideos",
    "arroz",
    "azucar",
    "gaseosa",
    "galletitas",
    "harina",
    "detergente",
    "manteca",
]


def scrape_all(
    terms: list[str] | None = None,
    stores: dict[str, str] | None = None,
) -> list[Product]:
    """Scrapea todas las tiendas para la canasta de términos.

    Resiliente: si una tienda o término falla, lo informa y sigue con el resto.
    Deduplica por (tienda, url, nombre).
    """
    terms = terms or DEFAULT_TERMS
    stores = stores or STORES
    seen: set[tuple] = set()
    products: list[Product] = []
    for store, host in stores.items():
        for term in terms:
            try:
                found = vtex.fetch(host, store, term)
            except Exception as exc:  # noqa: BLE001 - reportar y continuar
                print(f"[{store}] '{term}': {exc}")
                continue
            for p in found:
                key = (store, p.url, p.name)
                if key in seen:
                    continue
                seen.add(key)
                products.append(p)
    return products


__all__ = ["Product", "STORES", "DEFAULT_TERMS", "scrape_all", "vtex"]
