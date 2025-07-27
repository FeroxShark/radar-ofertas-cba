from pathlib import Path
from scraper import carrefour


def test_parse_fixture():
    html = Path('tests/fixtures/carrefour.html').read_text()
    products = carrefour.scrape(html)
    assert len(products) == 1
    p = products[0]
    assert p.name == 'Leche'
    assert p.brand == 'Marca'
    assert p.size_ml == 1000
    assert p.price_ars == 123.45
    assert p.url == 'https://carrefour.example.com/leche'
