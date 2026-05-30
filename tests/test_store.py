from datetime import datetime

from logic.store import append_prices, load_prices
from scraper.base import Product


def _product(name):
    return Product(
        name=name,
        brand="X",
        size_ml=1000,
        price_ars=100.0,
        url="u",
        store="Día",
        ts=datetime.utcnow(),
    )


def test_load_prices_missing_returns_empty(tmp_path):
    assert load_prices(tmp_path / "nope.json") == []


def test_append_prices_persists_and_accumulates(tmp_path):
    path = tmp_path / "prices.json"

    saved = append_prices([_product("Leche"), _product("Café")], path)
    assert saved == 2

    append_prices([_product("Yerba")], path)
    history = load_prices(path)
    assert len(history) == 3
    assert {r["name"] for r in history} == {"Leche", "Café", "Yerba"}
    assert history[0]["store"] == "Día"
