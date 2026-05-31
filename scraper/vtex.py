"""Cliente para tiendas montadas sobre la plataforma VTEX.

VTEX expone una API pública de catálogo (sin autenticación):

    GET {host}/api/catalog_system/pub/products/search?ft={termino}&_from=0&_to=49

Devuelve una lista de productos en JSON, cada uno con sus variantes (`items`) y
ofertas comerciales (`commertialOffer`, sí, así está escrito en VTEX) que
incluyen `Price` (precio actual) y `ListPrice` (precio de lista).
"""
from __future__ import annotations

from datetime import datetime

import requests

from .base import Product

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def _product_url(host: str, raw: dict) -> str:
    if raw.get("link"):
        return raw["link"]
    slug = raw.get("linkText")
    return f"{host}/{slug}/p" if slug else host


def parse_products(raw: list[dict], store: str, host: str) -> list[Product]:
    """Convierte la respuesta JSON de VTEX en una lista de `Product`."""
    products: list[Product] = []
    now = datetime.utcnow()
    for entry in raw:
        brand = entry.get("brand") or None
        url = _product_url(host, entry)
        for item in entry.get("items", []):
            offer = next(
                (
                    s.get("commertialOffer", {})
                    for s in item.get("sellers", [])
                    if s.get("commertialOffer", {}).get("IsAvailable")
                ),
                None,
            )
            if not offer:
                continue
            price = offer.get("Price")
            if not price:
                continue
            list_price = offer.get("ListPrice") or None
            products.append(
                Product(
                    name=item.get("name") or entry.get("productName") or "",
                    brand=brand,
                    price_ars=float(price),
                    list_price=float(list_price) if list_price else None,
                    url=url,
                    store=store,
                    ts=now,
                )
            )
    return products


def fetch(
    host: str,
    store: str,
    term: str,
    session: requests.Session | None = None,
    page_size: int = 50,
) -> list[Product]:
    """Busca `term` en una tienda VTEX y devuelve sus productos disponibles."""
    getter = session.get if session is not None else requests.get
    url = f"{host}/api/catalog_system/pub/products/search"
    params = {"ft": term, "_from": 0, "_to": page_size - 1}
    resp = getter(url, params=params, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return parse_products(resp.json(), store, host)
