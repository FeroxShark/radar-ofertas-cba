from datetime import datetime, timedelta

from logic import rank


def _rec(name, price, store, size=1000, ts=None):
    return {
        "name": name,
        "brand": "X",
        "size_ml": size,
        "price_ars": price,
        "url": "u",
        "store": store,
        "ts": (ts or datetime.utcnow()).isoformat(),
    }


def test_generate_deals_empty():
    assert rank.generate_deals([]) == []


def test_generate_deals_ranks_by_savings():
    records = [
        _rec("A", 100, "Día"),
        _rec("A", 200, "Jumbo"),
        _rec("B", 50, "Día"),
    ]
    deals = rank.generate_deals(records)
    assert len(deals) == 3
    # El más barato de A (100 vs promedio 150) es la mejor oferta.
    assert deals[0].name == "A"
    assert deals[0].price_ars == 100
    assert deals[0].savings_pct >= deals[-1].savings_pct


def test_generate_deals_respects_top_n():
    records = [_rec(f"P{i}", 100 + i, "Día") for i in range(5)]
    assert len(rank.generate_deals(records, top_n=2)) == 2


def test_generate_deals_ignores_old_records():
    old = datetime.utcnow() - timedelta(days=400)
    deals = rank.generate_deals([_rec("A", 100, "Día", ts=old)])
    assert deals == []
