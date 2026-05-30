"""Datos de muestra para demostrar la web sin scrapear tiendas reales."""
from __future__ import annotations

from datetime import datetime, timedelta

from scraper.base import Product

# (nombre, marca, tamaño_ml, [(tienda, precio), ...])
_CATALOG = [
    ("Leche entera 1L", "La Serenísima", 1000,
     [("Carrefour", 1290), ("Día", 980), ("Jumbo", 1350)]),
    ("Aceite de girasol 900ml", "Natura", 900,
     [("Carrefour", 2450), ("Día", 2890), ("Jumbo", 1990)]),
    ("Coca-Cola 2.25L", "Coca-Cola", 2250,
     [("Carrefour", 2990), ("Jumbo", 3290), ("MercadoLibre", 2490)]),
    ("Yerba mate 1kg", "Playadito", None,
     [("Carrefour", 3890), ("Día", 3290), ("Jumbo", 4100)]),
    ("Café molido 250g", "La Virginia", None,
     [("Carrefour", 3450), ("Día", 2990), ("MercadoLibre", 3800)]),
    ("Fideos tirabuzón 500g", "Lucchetti", None,
     [("Carrefour", 1190), ("Día", 950), ("Jumbo", 1290)]),
    ("Arroz largo fino 1kg", "Gallo", None,
     [("Carrefour", 1650), ("Día", 1490), ("Jumbo", 1890)]),
    ("Azúcar 1kg", "Ledesma", None,
     [("Carrefour", 1290), ("Día", 1190), ("Jumbo", 1390)]),
    ("Gaseosa lima-limón 2.25L", "Sprite", 2250,
     [("Carrefour", 2790), ("Jumbo", 2990)]),
    ("Detergente 750ml", "Magistral", 750,
     [("Carrefour", 2190), ("Día", 1790), ("MercadoLibre", 2390)]),
    ("Galletitas surtidas 400g", "Bagley", None,
     [("Carrefour", 1890), ("Día", 1690)]),
    ("Harina 0000 1kg", "Pureza", None,
     [("Carrefour", 990), ("Día", 850), ("Jumbo", 1090)]),
]


def sample_products() -> list[Product]:
    now = datetime.utcnow()
    products: list[Product] = []
    for i, (name, brand, size, offers) in enumerate(_CATALOG):
        for store, price in offers:
            slug = name.split()[0].lower()
            products.append(
                Product(
                    name=name,
                    brand=brand,
                    size_ml=size,
                    price_ars=float(price),
                    url=f"https://{store.lower()}.example.com/{slug}",
                    store=store,
                    ts=now - timedelta(hours=i),
                )
            )
    return products
