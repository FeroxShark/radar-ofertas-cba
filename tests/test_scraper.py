from pathlib import Path
from scraper import carrefour


def test_scrape_returns_list():
    html = Path('tests/fixtures/carrefour.html').read_text()
    products = carrefour.scrape(html)
    assert isinstance(products, list)
    assert products[0].name == 'Leche'
