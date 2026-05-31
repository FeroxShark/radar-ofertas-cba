from datetime import datetime

from logic.sample import sample_products
from logic.rank import Deal, generate_deals
from web.render import render_page


def test_render_page_writes_self_contained_html(tmp_path):
    records = [p.model_dump(mode="json") for p in sample_products()]
    deals = generate_deals(records)
    out = render_page(deals, tmp_path / "index.html")

    html = out.read_text(encoding="utf-8")
    assert html.startswith("<!DOCTYPE html>")
    assert "Radar de Ofertas" in html
    assert "const DEALS = [" in html
    # Los datos quedan embebidos: no hay fetch externo.
    assert "fetch(" not in html


def test_render_neutralizes_malicious_scraped_fields(tmp_path):
    evil = Deal(
        name="</script><img src=x onerror=alert(1)>",
        brand="<b>",
        price_ars=100,
        list_price=200,
        url="javascript:alert(1)",
        store="<x>",
        ts=datetime.utcnow(),
        savings_pct=50,
    )
    html = render_page([evil], tmp_path / "index.html").read_text(encoding="utf-8")
    # El "</script>" de los datos no cierra el bloque real (solo queda el del template).
    assert html.count("</script>") == 1
    # El marcado del nombre quedó neutralizado en el embed (< -> \\u003c).
    assert "<img src=x" not in html
