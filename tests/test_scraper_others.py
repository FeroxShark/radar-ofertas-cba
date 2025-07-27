from pathlib import Path

from scraper import dia, jumbo, mercadolibre


def read(name: str) -> str:
    return Path(f'tests/fixtures/{name}.html').read_text()


def test_dia():
    products = dia.scrape(read('dia'))
    assert products[0].name == 'Fideos'


def test_jumbo():
    products = jumbo.scrape(read('jumbo'))
    assert products[0].name == 'Cafe'


def test_mercadolibre():
    products = mercadolibre.scrape(read('mercadolibre'))
    assert products[0].name == 'Yerba'
