from datetime import datetime

from logic import rank


def test_generate_top20_empty(tmp_path):
    class DummyDB:
        def collection(self, name):
            class Coll:
                def where(self, *args, **kwargs):
                    return self

                def stream(self):
                    return []

            return Coll()

    result = rank.generate_top20(DummyDB(), tmp_path)
    assert result == []


def test_generate_top20_basic(tmp_path):
    now = datetime.utcnow()
    docs = [
        {
            "name": "A",
            "brand": "X",
            "size_ml": 1000,
            "price_ars": 100,
            "url": "u",
            "ts": now,
        },
        {
            "name": "A",
            "brand": "X",
            "size_ml": 1000,
            "price_ars": 200,
            "url": "u",
            "ts": now,
        },
        {
            "name": "B",
            "brand": "Y",
            "size_ml": 500,
            "price_ars": 50,
            "url": "u",
            "ts": now,
        },
    ]

    class Doc:
        def __init__(self, d):
            self._d = d

        def to_dict(self):
            return self._d

    class DummyDB:
        def collection(self, name):
            class Coll:
                def where(self, *args, **kwargs):
                    return self

                def stream(self):
                    return [Doc(d) for d in docs]

            return Coll()

    top = rank.generate_top20(DummyDB(), tmp_path)
    assert len(top) == 3
    assert top[0].savings_pct >= top[-1].savings_pct
