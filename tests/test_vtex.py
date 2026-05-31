import json
from pathlib import Path

from scraper import vtex

RAW = json.loads(Path("tests/fixtures/vtex_search.json").read_text())


def test_parse_products_extracts_available_offers():
    products = vtex.parse_products(RAW, "Carrefour", "https://www.carrefour.com.ar")
    # Se ignora el producto sin stock; quedan los dos disponibles.
    assert len(products) == 2
    by_name = {p.name: p for p in products}

    leche = by_name["Leche Entera 1L"]
    assert leche.price_ars == 980
    assert leche.list_price == 1290
    assert leche.store == "Carrefour"
    assert leche.brand == "La Serenísima"
    assert leche.url == "https://www.carrefour.com.ar/leche-entera-1l/p"


def test_parse_products_builds_url_from_slug():
    products = vtex.parse_products(RAW, "Día", "https://dia.example")
    desc = next(p for p in products if p.name == "Leche Descremada 1L")
    assert desc.url == "https://dia.example/leche-descremada-1l/p"


def test_fetch_uses_session_and_catalog_endpoint():
    calls = {}

    class FakeResp:
        def raise_for_status(self):
            calls["raised"] = True

        def json(self):
            return RAW

    class FakeSession:
        def get(self, url, params=None, headers=None, timeout=None):
            calls["url"] = url
            calls["params"] = params
            return FakeResp()

    products = vtex.fetch(
        "https://www.carrefour.com.ar", "Carrefour", "leche", session=FakeSession()
    )
    assert calls["url"].endswith("/api/catalog_system/pub/products/search")
    assert calls["params"]["ft"] == "leche"
    assert calls["raised"] is True
    assert len(products) == 2
