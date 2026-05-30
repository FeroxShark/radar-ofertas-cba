from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import json
from collections import defaultdict

from pydantic import BaseModel

import config


class Deal(BaseModel):
    name: str
    brand: str | None = None
    size_ml: int | None = None
    price_ars: float
    price_unit: float
    url: str
    ts: datetime
    savings_pct: float


def generate_top20(db, output_dir: Path) -> list[Deal]:
    since = datetime.utcnow() - timedelta(days=config.PRICE_WINDOW_DAYS)
    docs = db.collection('prices').where('ts', '>=', since).stream()
    items = []
    for doc in docs:
        data = doc.to_dict()
        size = data.get('size_ml') or 1
        unit = data['price_ars'] / size
        items.append({**data, 'price_unit': unit})

    avg = defaultdict(list)
    for it in items:
        avg[it['name']].append(it['price_unit'])

    averages = {k: sum(v) / len(v) for k, v in avg.items()}

    deals: list[Deal] = []
    for it in items:
        mean = averages[it['name']]
        savings = 0.0
        if mean:
            savings = (mean - it['price_unit']) / mean * 100
        deals.append(
            Deal(
                name=it['name'],
                brand=it.get('brand'),
                size_ml=it.get('size_ml'),
                price_ars=it['price_ars'],
                price_unit=it['price_unit'],
                url=it['url'],
                ts=it['ts'],
                savings_pct=savings,
            )
        )

    deals.sort(key=lambda d: d.savings_pct, reverse=True)
    top = deals[:config.TOP_N]
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{datetime.utcnow().date()}.json"
    path.write_text(json.dumps([d.model_dump() for d in top], default=str, indent=2))
    return top
