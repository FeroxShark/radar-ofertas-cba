from __future__ import annotations

import re

from .base import Product, build_scraper

URL = "https://dia.example.com"

PRODUCT_RE = re.compile(
    r'<li class="item"\s+data-name="(?P<name>[^"]+)"\s+'
    r'data-brand="(?P<brand>[^"]*)"\s+'
    r'data-size="(?P<size>\d+)"\s+'
    r'data-price="(?P<price>[\d,.]+)"[^>]*>\s*'
    r'<a href="(?P<url>[^"]+)"',
    re.S,
)

scrape = build_scraper(URL, PRODUCT_RE, store="Día")

__all__ = ["Product", "URL", "PRODUCT_RE", "scrape"]
