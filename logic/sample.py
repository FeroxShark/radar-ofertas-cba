"""Datos de muestra para demostrar la web sin scrapear tiendas reales."""
from __future__ import annotations

from datetime import datetime, timedelta

from scraper.base import Product

# (nombre, marca, tamaño_ml, tienda, precio_actual, precio_lista)
_CATALOG = [
    ("Leche entera 1L", "La Serenísima", 1000, "Día", 980, 1290),
    ("Aceite de girasol 900ml", "Natura", 900, "Carrefour", 1990, 2650),
    ("Coca-Cola 2.25L", "Coca-Cola", 2250, "Carrefour", 2490, 2990),
    ("Yerba mate 1kg", "Playadito", None, "Día", 3290, 3990),
    ("Café molido 250g", "La Virginia", None, "Carrefour", 2990, 3450),
    ("Fideos tirabuzón 500g", "Lucchetti", None, "Día", 950, 1190),
    ("Arroz largo fino 1kg", "Gallo", None, "Día", 1490, 1790),
    ("Azúcar 1kg", "Ledesma", None, "Carrefour", 1190, 1390),
    ("Gaseosa lima-limón 2.25L", "Sprite", 2250, "Carrefour", 2290, 2990),
    ("Detergente 750ml", "Magistral", 750, "Día", 1790, 2390),
    ("Galletitas surtidas 400g", "Bagley", None, "Día", 1290, 1690),
    ("Harina 0000 1kg", "Pureza", None, "Día", 850, 990),
    ("Manteca 200g", "La Paulina", None, "Carrefour", 1390, 1690),
    ("Atún al natural 170g", "La Campagnola", None, "Día", 1490, 1990),
]


def sample_products() -> list[Product]:
    now = datetime.utcnow()
    products: list[Product] = []
    for i, (name, brand, size, store, price, list_price) in enumerate(_CATALOG):
        slug = name.split()[0].lower()
        products.append(
            Product(
                name=name,
                brand=brand,
                size_ml=size,
                price_ars=float(price),
                list_price=float(list_price),
                url=f"https://{store.lower()}.example.com/{slug}",
                store=store,
                ts=now - timedelta(hours=i),
            )
        )
    return products
