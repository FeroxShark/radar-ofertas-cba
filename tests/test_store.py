from datetime import datetime

from logic.store import save_products
from scraper.base import Product


class DummyCollection:
    def __init__(self):
        self.added = []
        self.docs = {}

    def add(self, data):
        self.added.append(data)

    def document(self, name):
        doc = self.docs.setdefault(name, DummyDoc())
        return doc


class DummyDoc:
    def __init__(self):
        self.data = None

    def set(self, data, merge=False):
        self.data = data


class DummyDB:
    def __init__(self):
        self.collections = {}

    def collection(self, name):
        return self.collections.setdefault(name, DummyCollection())


def _product(name):
    return Product(
        name=name,
        brand="X",
        size_ml=1000,
        price_ars=100.0,
        url="u",
        ts=datetime.utcnow(),
    )


def test_save_products_writes_prices_and_log():
    db = DummyDB()
    products = [_product("Leche"), _product("Cafe")]

    saved = save_products(db, products, retailer="carrefour")

    assert saved == 2
    assert len(db.collection("prices").added) == 2
    assert db.collection("prices").added[0]["name"] == "Leche"
    log = db.collection("scraper_logs").document("carrefour")
    assert log.data["count"] == 2
    assert isinstance(log.data["ts"], datetime)


def test_save_products_without_retailer_skips_log():
    db = DummyDB()
    saved = save_products(db, [_product("Yerba")])
    assert saved == 1
    assert db.collection("scraper_logs").docs == {}
