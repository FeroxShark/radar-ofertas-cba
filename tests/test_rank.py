from datetime import datetime, timedelta

from logic import rank


def _rec(name, price, list_price, store="Día", size=None, ts=None, url=None):
    return {
        "name": name,
        "brand": "X",
        "size_ml": size,
        "price_ars": price,
        "list_price": list_price,
        "url": url or f"https://t/{name}",
        "store": store,
        "ts": (ts or datetime.utcnow()).isoformat(),
    }


def test_generate_deals_empty():
    assert rank.generate_deals([]) == []


def test_generate_deals_only_real_offers():
    records = [
        _rec("Con descuento", 800, 1000),   # 20% off
        _rec("Sin descuento", 1000, 1000),  # 0% -> se ignora
        _rec("Sin lista", 500, None),       # sin precio de lista -> se ignora
    ]
    deals = rank.generate_deals(records)
    assert len(deals) == 1
    assert deals[0].name == "Con descuento"
    assert round(deals[0].savings_pct) == 20


def test_generate_deals_sorted_by_savings():
    records = [
        _rec("A", 900, 1000),   # 10%
        _rec("B", 500, 1000),   # 50%
        _rec("C", 800, 1000),   # 20%
    ]
    deals = rank.generate_deals(records)
    assert [d.name for d in deals] == ["B", "C", "A"]


def test_generate_deals_respects_top_n():
    records = [_rec(f"P{i}", 100, 200) for i in range(5)]
    assert len(rank.generate_deals(records, top_n=2)) == 2


def test_generate_deals_ignores_old_records():
    old = datetime.utcnow() - timedelta(days=400)
    deals = rank.generate_deals([_rec("A", 800, 1000, ts=old)])
    assert deals == []


def test_generate_deals_uses_latest_snapshot_per_product():
    old = datetime.utcnow() - timedelta(days=3)
    new = datetime.utcnow()
    # Mismo producto (misma url): el snapshot viejo tenía 50% off, el nuevo no.
    records = [
        _rec("Leche", 500, 1000, ts=old, url="https://t/leche"),
        _rec("Leche", 1000, 1000, ts=new, url="https://t/leche"),
    ]
    # Gana el snapshot más reciente (sin descuento) -> no aparece como oferta.
    assert rank.generate_deals(records) == []
